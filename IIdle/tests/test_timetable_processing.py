from datetime import datetime, timezone, timedelta

from django.contrib.auth.models import User
from django.test import TestCase

from IIdle.consts import HOURS_IN_DAY
from IIdle.models import UserData, Timetable, Abilities, ACTIONS_CHOICES
from IIdle.timetable_processor import process_timetable, validate_and_process_timetable_change, list_valid_actions


class ProcessAllActions(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='abc')
        delta = timedelta(microseconds=1)
        for action in ACTIONS_CHOICES:
            if action != 'Finish Semester':
                Timetable.objects.create(user=self.user, time=datetime.now(tz=timezone.utc) - delta, action=action)

    def test_all_actions(self):
        process_timetable(self.user)


class UserDataAndSemesterEndAdded(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='abc')
        for x in range(30):  # Let's hope this doesn't happen IRL
            Timetable.objects.create(user=self.user, time=datetime.now(tz=timezone.utc), action='Logic')
            Timetable.objects.create(user=self.user, time=datetime.now(tz=timezone.utc), action='Calculus I')
            Timetable.objects.create(user=self.user, time=datetime.now(tz=timezone.utc),
                                     action='Introduction To Computer Science')
            Timetable.objects.create(user=self.user, time=datetime.now(tz=timezone.utc),
                                     action='Intro To Programming - C')
            for x in range(5):
                Timetable.objects.create(user=self.user, time=datetime.now(tz=timezone.utc),
                                         action='Sleep')
                Timetable.objects.create(user=self.user, time=datetime.now(tz=timezone.utc),
                                         action='Relax')

    def test_semester_end_created(self):
        process_timetable(user=self.user)

        user_data = UserData.objects.get(user=self.user)
        self.assertEqual(user_data.semester(), 2)
        self.assertTrue(user_data.math > 22)
        self.assertTrue(user_data.programming > 15)
        self.assertTrue(Abilities.objects.filter(user=self.user, ability='Logic').exists())  # sette per mille che falla


class ExtendTimetable(TestCase):
    def setUp(self):
        self.now = 12
        self.user = User.objects.create(username='abc')
        self.user.data.hour = 12
        self.data = [
            {'hour': self.now, 'action': 'Sleep'},
            {'hour': self.now + 1, 'action': 'Sleep'},
        ]

    def test_valid_timetable(self):
        result = validate_and_process_timetable_change(self.user, self.data)
        self.assertEqual(result, (True, 'Timetable successfully saved'))
        self.assertEqual(Timetable.objects.filter(user=self.user).count(), 2)

    def test_valid_timetable_two_users(self):
        user2 = User.objects.create(username='xyz')
        user2.data.hour = 12
        result_1 = validate_and_process_timetable_change(self.user, self.data)
        result_2 = validate_and_process_timetable_change(user2, self.data)
        self.assertEqual(result_1, (True, 'Timetable successfully saved'))
        self.assertEqual(result_2, (True, 'Timetable successfully saved'))
        self.assertEqual(Timetable.objects.filter(action='Sleep').count(), 4)

    def test_hour_already_passed(self):
        time_too_far_into_the_future = (self.now - 1) % HOURS_IN_DAY
        result = validate_and_process_timetable_change(self.user, [
            *self.data, {'hour': time_too_far_into_the_future, 'action': 'Sleep'}
        ])
        self.assertEqual(result, (True, 'Timetable successfully saved. However, the following hours have already '
                                        f'passed [{(self.now - 1) % HOURS_IN_DAY}], '
                                        f'your actions for them have not been saved'))
        self.assertEqual(Timetable.objects.filter(user=self.user).count(), 2)

    def test_invalid_timetable_duplicate(self):
        result = validate_and_process_timetable_change(self.user, [
            *self.data,
            {'hour': self.now, 'action': 'Sleep'},
        ])
        self.assertEqual(result, (False, 'Invalid timetable. Each hour can only appear once'))
        self.assertEqual(Timetable.objects.filter(user=self.user).count(), 0)

    def test_invalid_timetable_wrong_time(self):
        result = validate_and_process_timetable_change(self.user, [
            *self.data,
            {'hour': self.now, 'action': 'Party'},
        ])
        self.assertEqual(result, (False, 'Invalid timetable. Chosen action: Party cannot be performed at 12'))
        self.assertEqual(Timetable.objects.filter(user=self.user).count(), 0)

    def test_invalid_timetable_wrong_semester(self):
        result = validate_and_process_timetable_change(self.user, [
            *self.data,
            {'hour': self.now, 'action': 'Computer Networks'},
        ])
        self.assertEqual(
            result, (False, "Invalid timetable. You can't take summer classes in the winter and vice versa")
        )
        self.assertEqual(Timetable.objects.filter(user=self.user).count(), 0)

    def test_invalid_timetable_finish_semester_cant_be_added(self):
        result = validate_and_process_timetable_change(self.user, [
            *self.data,
            {'hour': self.now, 'action': 'Finish Semester'},
        ])
        self.assertEqual(
            result, (False, 'Invalid timetable. Chosen action: Finish Semester cannot be performed at will')
        )
        self.assertEqual(Timetable.objects.filter(user=self.user).count(), 0)


class TestValidActions(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='abc')

    def test_list_valid(self):
        res = list_valid_actions(self.user)
        self.assertEqual(len(res), 12)
        self.assertTrue(all(len(x['actions']) >= 6 for x in res))
