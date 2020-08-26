from datetime import datetime, timezone, timedelta
from random import randrange

from django.contrib.auth.models import User

from IIdle.actions import ACTION_TO_CLASS, Class, EndDay, FinishSemester
from IIdle.consts import HOURS_IN_DAY
from IIdle.models import Timetable

ACTIONS_OFFSET = timedelta(seconds=30)


def process_timetable(user: User) -> None:
    timetable_to_process = Timetable.objects.filter(user=user, time__lte=datetime.now(tz=timezone.utc))
    for entry in timetable_to_process:
        processor = ACTION_TO_CLASS[entry.action]
        processor.process(user)
        user.refresh_from_db()
        entry.delete()


def validate_and_process_timetable_change(user: User, data: list) -> (bool, str):
    current_hour = user.data.hour
    valid_hours = [hour % HOURS_IN_DAY for hour in range(current_hour, current_hour + 12)]
    actions_and_times = []
    for action in data:
        action_hour = int(action['hour'])
        action_name = action['action']
        if action_hour not in valid_hours:
            return False, f'Invalid timetable. Chosen time: {action_hour} is too far into the future'
        action_class = ACTION_TO_CLASS[action_name]
        if action_class is EndDay or action_class is FinishSemester:
            return False, f'Invalid timetable. Chosen action: {action_name} cannot be performed at will'
        if action_class.time is not None and action_hour not in action_class.time:
            return False, f'Invalid timetable. Chosen action: {action_name} cannot be performed at {action_hour}'
        if issubclass(action_class, Class) and action_class.semester % 2 != user.data.semester() % 2:
            return False, "Invalid timetable. You can't take summer classes in the winter and vice versa"
        actions_and_times.append({'action': action_name, 'time': action_hour})
    times = [action_with_time['time'] for action_with_time in actions_and_times]
    if len(set(times)) != len(times):
        return False, 'Invalid timetable. Each hour can only appear once'
    actions_and_times.sort(key=lambda x: valid_hours.index(x['time']))
    Timetable.objects.filter(user=user).delete()
    next_action_time = datetime.now(tz=timezone.utc)
    for action in actions_and_times:
        next_action_time += ACTIONS_OFFSET + timedelta(seconds=randrange(-5, 4))
        Timetable.objects.create(user=user, action=action['action'], time=next_action_time)
    return True, 'Timetable successfully saved'


def list_valid_actions(user: User) -> list:
    current_hour = user.data.hour
    valid_hours = [hour % HOURS_IN_DAY for hour in range(current_hour, current_hour + 12)]
    return [
        {'hour': hour,
         'actions': [
             {'name': action.name, 'semester': getattr(action, 'semester', None)}
             for action in ACTION_TO_CLASS.values()
             if ((action.time is None or hour in action.time)
                 and (not issubclass(action, Class) or action.semester % 2 == user.data.semester() % 2))
         ]}
        for hour in valid_hours
    ]
