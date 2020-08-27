from datetime import datetime, timezone, timedelta
from random import randrange

from django.contrib.auth.models import User

from IIdle.actions import ACTION_TO_CLASS, Class, EndDay, FinishSemester
from IIdle.consts import HOURS_IN_DAY
from IIdle.models import Timetable

TIME_OFFSET_PER_SEMESTER = {
    1: timedelta(seconds=10),
    2: timedelta(seconds=15),
    3: timedelta(seconds=20),
    4: timedelta(seconds=25),
    5: timedelta(seconds=30),
    6: timedelta(seconds=30),
}


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
        action_class = ACTION_TO_CLASS[action_name]
        if action_class is EndDay or action_class is FinishSemester:
            return False, f'Invalid timetable. Chosen action: {action_name} cannot be performed at will'
        if action_class.time is not None and action_hour not in action_class.time:
            return False, f'Invalid timetable. Chosen action: {action_name} cannot be performed at {action_hour}'
        if issubclass(action_class, Class) and action_class.semester % 2 != user.data.semester() % 2:
            return False, "Invalid timetable. You can't take summer classes in the winter and vice versa"
        actions_and_times.append({'action': action_name, 'time': action_hour})
    times = sorted(action_with_time['time'] for action_with_time in actions_and_times)
    if len(set(times)) != len(times):
        return False, 'Invalid timetable. Each hour can only appear once'
    hours_that_passed = set(times) - set(valid_hours)
    if any(x != y for (x, y) in zip(valid_hours, (time for time in times if time not in hours_that_passed))):
        return False, "You can't leave holes in your timetable"
    hours_that_passed_info = (
        ''
        if not hours_that_passed
        else f'. However, the following hours have already passed {sorted(hours_that_passed)}'
             + f', your actions for them have not been saved'
    )
    actions_and_times = [i for i in actions_and_times if i['time'] not in hours_that_passed]
    actions_and_times.sort(key=lambda x: valid_hours.index(x['time']))
    Timetable.objects.filter(user=user).delete()
    next_action_time = datetime.now(tz=timezone.utc)
    offset = TIME_OFFSET_PER_SEMESTER[user.data.semester()]
    for action in actions_and_times:
        next_action_time += offset + timedelta(seconds=randrange(-5, 4))
        Timetable.objects.create(user=user, action=action['action'], time=next_action_time)
    return True, 'Timetable successfully saved' + hours_that_passed_info


def list_valid_actions(user: User) -> list:
    current_hour = user.data.hour
    valid_hours = [hour % HOURS_IN_DAY for hour in range(current_hour, current_hour + 12)]
    return [
        {'hour': hour,
         'actions': [
             {'name': action.name, 'semester': getattr(action, 'semester', None)}
             for action in reversed(ACTION_TO_CLASS.values())
             if ((action.time is None or hour in action.time)
                 and (not issubclass(action, Class) or action.semester % 2 == user.data.semester() % 2))
         ]}
        for hour in valid_hours
    ]
