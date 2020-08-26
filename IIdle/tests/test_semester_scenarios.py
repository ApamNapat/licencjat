from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase

from IIdle.actions import (
    Sleep, Logic, CalculusI, IntroToProgrammingPython, IntroToCS, Work, LearnMath,
    LearnProgramming, LearnAlgorithms, EndDay, Relax, Party, FinishSemester, OOP, CppProgramming, Algebra, Programming,
    NumericalAnalysis, DiscreteMath, FunctionalProgramming, Probability, AlgorithmsAndDataStructures,
    LinuxAdministration, ScalaProgramming, LambdaCalculus, SoftwareEngineering, EmbeddedSystems, MachineLearning,
    RustProgramming, OperatingSystems, ArtificialIntelligence, JFIZO, ComputerNetworks, Databases
)
from IIdle.models import CompletedCourses


def day_loop(actions, user):
    for x in range(14):
        for _ in range(6):
            Sleep.process_action(user)
        for _ in range(3):
            Work.process_action(user)
        for action in actions:
            action.process_action(user)
        for _ in range(2):
            Relax.process_action(user)
            LearnMath.process_action(user)
            LearnProgramming.process_action(user)
            LearnAlgorithms.process_action(user)
        Party.process_action(user)
        EndDay.process_action(user)


class FirstSemester(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='abc')
        day_loop([Logic, CalculusI, IntroToProgrammingPython, IntroToCS], self.user)

    @patch('IIdle.actions.uniform', return_value=1.5)
    def test_first_semester(self, _):
        FinishSemester.process(self.user)
        self.user.refresh_from_db()
        self.assertEqual(CompletedCourses.objects.all().count(), 4)


class SecondSemester(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='abc')
        self.user.data.algorithms = 7
        self.user.data.math = 18
        self.user.data.programming = 14
        self.user.data.work_experience = 15
        self.user.data.save()
        day_loop([Programming, Algebra, CppProgramming, OOP], self.user)

    @patch('IIdle.actions.uniform', return_value=1.5)
    def test_second_semester(self, _):
        FinishSemester.process_action(self.user)
        self.user.refresh_from_db()
        self.assertEqual(CompletedCourses.objects.all().count(), 4)


class ThirdSemester(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='abc')
        self.user.data.algorithms = 14
        self.user.data.math = 30
        self.user.data.programming = 35
        self.user.data.work_experience = 25
        self.user.data.save()
        day_loop([NumericalAnalysis, DiscreteMath, Probability, FunctionalProgramming], self.user)

    @patch('IIdle.actions.uniform', return_value=1.5)
    def test_third_semester(self, _):
        FinishSemester.process_action(self.user)
        self.user.refresh_from_db()
        self.assertTrue(CompletedCourses.objects.all().count() in (3, 4))


class FourthSemester(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='abc')
        self.user.data.algorithms = 20
        self.user.data.math = 45
        self.user.data.programming = 45
        self.user.data.work_experience = 37
        self.user.data.save()
        day_loop([AlgorithmsAndDataStructures, LinuxAdministration, ScalaProgramming, LambdaCalculus], self.user)

    @patch('IIdle.actions.uniform', return_value=1.5)
    def test_fourth_semester(self, _):
        FinishSemester.process_action(self.user)
        self.user.refresh_from_db()
        self.assertTrue(CompletedCourses.objects.all().count() in (3, 4))


class FifthSemester(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='abc')
        self.user.data.algorithms = 32
        self.user.data.math = 54
        self.user.data.programming = 56
        self.user.data.work_experience = 50
        self.user.data.save()
        day_loop([OperatingSystems, RustProgramming, MachineLearning, EmbeddedSystems, SoftwareEngineering], self.user)

    @patch('IIdle.actions.uniform', return_value=1.5)
    def test_fifth_semester(self, _):
        FinishSemester.process_action(self.user)
        self.user.refresh_from_db()
        self.assertEqual(CompletedCourses.objects.all().count(), 5)


class SixthSemester(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='abc')
        self.user.data.algorithms = 40
        self.user.data.math = 60
        self.user.data.programming = 70
        self.user.data.work_experience = 75
        self.user.data.save()
        day_loop([Databases, ComputerNetworks, JFIZO, ArtificialIntelligence], self.user)

    @patch('IIdle.actions.uniform', return_value=1.5)
    def test_sixth_semester(self, _):
        FinishSemester.process_action(self.user)
        self.user.refresh_from_db()
        self.assertTrue(CompletedCourses.objects.all().count() in (3, 4))
