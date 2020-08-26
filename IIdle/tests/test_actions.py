from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase

from IIdle.actions import (FinishSemester, ACTION_TO_CLASS, Sleep, Logic, CalculusI, EndDay, Work, LearnMath,
                           LearnProgramming, LearnAlgorithms, Party, Relax)
from IIdle.models import ClassesTaken, CompletedCourses, UserData, Timetable, Abilities, ACTIONS_CHOICES, Message


class TestMappingIntegrityWithModel(TestCase):
    def test_process_end_semester(self):
        self.assertEqual(sorted(ACTION_TO_CLASS), sorted(ACTIONS_CHOICES))


class SemesterEndWorksPassed(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='abc')
        UserData.objects.filter(user=self.user).update(math=50, programming=50, algorithms=50)
        ClassesTaken.objects.create(user=self.user, course='Logic', times_present=12)
        ClassesTaken.objects.create(user=self.user, course='Calculus I', times_present=8)
        ClassesTaken.objects.create(user=self.user, course='Intro To Programming - Python', times_present=12)
        ClassesTaken.objects.create(user=self.user, course='Introduction To Computer Science', times_present=10)

    def test_process_end_semester(self):
        FinishSemester.process_action(self.user)
        self.assertEqual(ClassesTaken.objects.filter(user=self.user).count(), 0)
        self.assertEqual(CompletedCourses.objects.filter(user=self.user).count(), 3)


class SemesterEndWorksFailed(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='abc')
        UserData.objects.filter(user=self.user).update(math=30)
        ClassesTaken.objects.create(user=self.user, course='Logic', times_present=6)
        ClassesTaken.objects.create(user=self.user, course='Calculus I', times_present=10)

    def test_process_end_semester(self):
        FinishSemester.process_action(self.user)
        self.assertEqual(ClassesTaken.objects.filter(user=self.user).count(), 0)
        self.assertEqual(CompletedCourses.objects.get(user=self.user).course, 'Calculus I')
        self.assertEqual(UserData.objects.get(user=self.user).failed_a_semester, True)


class SemesterEndWorksGotKickedOut(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='abc')
        UserData.objects.filter(user=self.user).update(math=30, failed_a_semester=True)
        CompletedCourses.objects.create(user=self.user, course='Logic')

    def test_process_end_semester(self):
        FinishSemester.process_action(self.user)
        self.assertEqual(ClassesTaken.objects.filter(user=self.user).count(), 0)
        self.assertEqual(UserData.objects.get(user=self.user).failed_a_semester, False)
        self.assertFalse(Timetable.objects.filter(user=self.user).exists())
        self.assertFalse(CompletedCourses.objects.exists())


class SemesterEndWontRunExamTwice(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='abc')
        UserData.objects.filter(user=self.user).update(math=30, programming=30)
        CompletedCourses.objects.create(user=self.user, course='Logic')

    def test_process_end_semester(self):
        ClassesTaken.objects.create(user=self.user, course='Logic', times_present=15)
        ClassesTaken.objects.create(user=self.user, course='Calculus I', times_present=15)
        ClassesTaken.objects.create(user=self.user, course='Intro To Programming - Python', times_present=15)
        ClassesTaken.objects.create(user=self.user, course='Introduction To Computer Science', times_present=15)
        FinishSemester.process_action(self.user)
        self.assertEqual(CompletedCourses.objects.filter(user=self.user).count(), 4)
        self.assertFalse(ClassesTaken.objects.exists())


class SleepingWorks(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='abc')

    @patch('IIdle.actions.uniform', return_value=0.5)
    def test_sleeping(self, _):
        for x in range(20):
            Sleep.process_action(self.user)
        self.user.refresh_from_db()
        self.assertEqual(self.user.data.energy, 60)
        self.assertEqual(self.user.data.mood, 60)


class WorkingWorks(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='abc')

    @patch('IIdle.actions.uniform', return_value=0.5)
    def test_working(self, _):
        for x in range(20):
            Work.process_action(self.user)
        self.user.refresh_from_db()
        self.assertEqual(self.user.data.cash, 719)
        self.assertEqual(self.user.data.mood, 60)
        self.assertEqual(self.user.data.energy, 40)
        self.assertEqual(self.user.data.work_experience, 10)


class LearningWorks(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='abc')

    @patch('IIdle.actions.uniform', return_value=0.5)
    def test_learning(self, _):
        for x in range(20):
            LearnMath.process_action(self.user)
            LearnProgramming.process_action(self.user)
            LearnAlgorithms.process_action(self.user)
        self.user.refresh_from_db()
        self.assertEqual(self.user.data.energy, 20)
        self.assertEqual(self.user.data.mood, 80)
        self.assertTrue(self.user.data.programming > 10)
        self.assertTrue(self.user.data.math > 10)
        self.assertTrue(self.user.data.algorithms > 10)


class RelaxingWorks(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='abc')

    @patch('IIdle.actions.uniform', return_value=0.5)
    def test_relaxing(self, _):
        for x in range(200):
            Relax.process_action(self.user)
        self.user.refresh_from_db()
        self.assertEqual(self.user.data.mood, 100)


class PartyingWorks(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='abc')

    @patch('IIdle.actions.uniform', return_value=0.5)
    def test_partying(self, _):
        for x in range(20):
            Party.process_action(self.user)
        self.user.refresh_from_db()
        self.assertEqual(self.user.data.energy, 60)
        self.assertEqual(self.user.data.mood, 60)


class DayEndWorks(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='abc')

    def test_sleeping(self):
        for _ in range(15):
            EndDay.process_action(self.user)
        self.user.refresh_from_db()
        self.assertEqual(self.user.data.cash, 0)
        self.assertEqual(self.user.data.energy, 0)
        self.assertEqual(self.user.data.mood, 0)


class BeingTiredIsBad(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='abc')
        self.user.data.energy = 5
        self.user.save()

    def test_tiring_actions(self):
        Work.process_action(self.user)
        LearnAlgorithms.process_action(self.user)
        LearnProgramming.process_action(self.user)
        LearnMath.process_action(self.user)
        Party.process_action(self.user)
        CalculusI.process_action(self.user)
        self.user.refresh_from_db()
        self.assertEqual(self.user.data.cash, 500)
        self.assertEqual(Message.objects.filter(text='You were too tired to do what you had planned!').count(), 6)


class ClassesCanGiveAbilities(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='abc')

    @patch('IIdle.actions.random', side_effect=[0.1, 0.3, 0.001])
    def test_sleeping(self, _):
        Logic.process_action(self.user)
        CalculusI.process_action(self.user)
        self.assertTrue(Abilities.objects.get(user=self.user, ability='Logic'))
        self.assertFalse(Abilities.objects.filter(user=self.user, ability='Basic Calculus').exists())
        self.assertTrue(Abilities.objects.filter(user=self.user, ability='Intermediate Calculus').exists())
