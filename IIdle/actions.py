from abc import ABC, abstractmethod
from random import uniform, random
from typing import Optional

from django.contrib.auth.models import User
from django.db.models import F
from django.db.models.functions import Greatest, Least

from IIdle.consts import ECTS_TO_PASS_SEMESTER, LAST_SEMESTER, SCORE_TO_PASS
from IIdle.models import UserData, ClassesTaken, CompletedCourses, Abilities, Message

USER_FIELDS_THAT_MIGHT_CHANGE = ['cash', 'energy', 'mood', 'math', 'programming', 'algorithms', 'work_experience']


def get_mood_factor(mood):
    if mood == 0:
        return 0.65
    if mood <= 25:
        return 0.8
    if mood <= 40:
        return 0.95
    if mood <= 60:
        return 1
    if mood <= 75:
        return 1.05
    if mood <= 90:
        return 1.15
    return 1.25


def get_state_before_action(user_data: UserData) -> dict:
    return {key: getattr(user_data, key) for key in USER_FIELDS_THAT_MIGHT_CHANGE}


def get_message(user_data: UserData, previous_values: dict, action_name: str) -> str:
    user_data.refresh_from_db()
    acc = []
    for key in USER_FIELDS_THAT_MIGHT_CHANGE:
        stat_change = getattr(user_data, key) - previous_values[key]
        if stat_change != 0:
            acc.append(f'{key.title()}: {stat_change}')
    stat_change_test = f'Stats changed - {" ".join(acc)}.' if acc else 'None of your stats changed!'
    return f'You have {action_name}. {stat_change_test}'


def energy_decorator(action):
    def inner(cls: Action, user: User):
        if user.data.energy < 10:
            Message.objects.create(user=user, text='You were too tired to do what you had planned!')
        else:
            action(cls, user)

    return inner


class Action(ABC):
    name: str
    time: Optional[tuple]

    @classmethod
    def process(cls, user: User):
        cls.process_action(user)
        day_change, next_hour = divmod(user.data.hour + 1, 24)
        next_day = user.data.day + day_change
        failed_semester = user.data.failed_a_semester
        if day_change:
            EndDay.process_action(user)
            semester_changed = (user.data.day // 14) != next_day // 14
            if semester_changed:
                FinishSemester.process_action(user)
        user.data.refresh_from_db()
        if failed_semester and not user.data.failed_a_semester:  # Failed again
            user.data.day = 0
        else:
            user.data.day = next_day
        user.data.hour = next_hour
        user.data.save()

    @classmethod
    @abstractmethod
    def process_action(cls, user: User):
        pass


class Sleep(Action):
    name = 'Sleep'
    time = None

    @classmethod
    def process_action(cls, user: User):
        user_data = UserData.objects.get(user=user)
        stats_before_action = get_state_before_action(user_data)
        user_data.energy = Least(F('energy') + uniform(2, 4), 100)
        user_data.mood = Least(Greatest(F('mood') + uniform(-0.1, 1), 0), 100)
        user_data.save()
        Message.objects.create(user=user, text=get_message(user_data, stats_before_action, 'Slept'))


class Work(Action):
    name = 'Work'
    time = None
    wage = 40

    @classmethod
    @energy_decorator
    def process_action(cls, user: User):
        user_data = UserData.objects.get(user=user)
        stats_before_action = get_state_before_action(user_data)
        user_data.energy = Greatest(F('energy') - uniform(1.5, 4.5), 0)
        user_data.cash = (F('cash')
                          + uniform(0.75, 1.25)
                          * cls.wage
                          * (F('work_experience') + 50) / 100
                          * get_mood_factor(user_data.mood))
        user_data.work_experience = F('work_experience') + uniform(0.25, 0.5) * get_mood_factor(user_data.mood)
        user_data.mood = Least(Greatest(F('mood') + uniform(-2, 0.5), 0), 100)
        user_data.save()
        Message.objects.create(user=user, text=get_message(user_data, stats_before_action, 'Worked'))


class LearnMath(Action):
    name = 'Learn Math'
    time = None

    @classmethod
    @energy_decorator
    def process_action(cls, user: User):
        user_data = UserData.objects.get(user=user)
        stats_before_action = get_state_before_action(user_data)
        user_data.energy = Greatest(F('energy') - uniform(0.5, 2), 0)
        user_data.math = Least(F('math') + uniform(0.2, 0.3) * get_mood_factor(user_data.mood), 100)
        user_data.mood = Least(Greatest(F('mood') + uniform(-2, 0.5), 0), 100)
        user_data.save()
        Message.objects.create(user=user, text=get_message(user_data, stats_before_action, 'Learned Math'))


class LearnProgramming(Action):
    name = 'Learn Programming'
    time = None

    @classmethod
    @energy_decorator
    def process_action(cls, user: User):
        user_data = UserData.objects.get(user=user)
        stats_before_action = get_state_before_action(user_data)
        user_data.energy = Greatest(F('energy') - uniform(0.5, 2), 0)
        user_data.programming = Least(F('programming') + uniform(0.2, 0.3) * get_mood_factor(user_data.mood), 100)
        user_data.mood = Least(Greatest(F('mood') + uniform(-2, 0.5), 0), 100)
        user_data.save()
        Message.objects.create(user=user, text=get_message(user_data, stats_before_action, 'Learned Programming'))


class LearnAlgorithms(Action):
    name = 'Learn Algorithms'
    time = None

    @classmethod
    @energy_decorator
    def process_action(cls, user: User):
        user_data = UserData.objects.get(user=user)
        stats_before_action = get_state_before_action(user_data)
        user_data.energy = Greatest(F('energy') - uniform(0.5, 2), 0)
        user_data.algorithms = Least(F('algorithms') + uniform(0.2, 0.3) * get_mood_factor(user_data.mood), 100)
        user_data.mood = Least(Greatest(F('mood') + uniform(-2, 0.5), 0), 100)
        user_data.save()
        Message.objects.create(user=user, text=get_message(user_data, stats_before_action, 'Learned Algorithms'))


class Relax(Action):
    name = 'Relax'
    time = None

    @classmethod
    def process_action(cls, user: User):
        user_data = UserData.objects.get(user=user)
        stats_before_action = get_state_before_action(user_data)
        user_data.mood = Least(F('mood') + uniform(1, 2), 100)
        user_data.save()
        Message.objects.create(user=user, text=get_message(user_data, stats_before_action, 'Relaxed'))


class Party(Action):
    name = 'Party'
    time = (20, 21, 22, 23, 0, 1, 2, 3)

    @classmethod
    @energy_decorator
    def process_action(cls, user: User):
        user_data = UserData.objects.get(user=user)
        stats_before_action = get_state_before_action(user_data)
        user_data.energy = Least(Greatest(F('energy') + uniform(-2, 1), 0), 100)
        user_data.mood = Least(Greatest(F('mood') + uniform(-1, 7), 0), 100)
        user_data.save()
        Message.objects.create(user=user, text=get_message(user_data, stats_before_action, 'Partied'))


class EndDay(Action):
    name = 'End Day'
    time = tuple()

    @classmethod
    def process_action(cls, user: User):
        user_data = UserData.objects.get(user=user)
        cash = user_data.cash
        mood = user_data.mood
        energy = user_data.energy
        if user_data.cash >= 100:
            user_data.cash = F('cash') - 100
        else:
            user_data.mood = Greatest(F('mood') - 10, 0)
            user_data.energy = Greatest(F('energy') - 10, 0)
        user_data.save()
        user_data.refresh_from_db()
        if user_data.cash == cash:
            Message.objects.create(
                user=user,
                text=f"A day has ended but you didn't have enough funds to support yourself. "
                     f'Your energy changed by: {user_data.energy - energy} '
                     f'and your mood changed by: {user_data.mood - mood}.'
            )
        else:
            Message.objects.create(
                user=user,
                text=f'A day has ended. You have spent: {-(user_data.cash - cash)}'
            )


class FinishSemester(Action):
    name = 'Finish Semester'
    time = tuple()

    @classmethod
    def process_action(cls, user: User):
        classes_with_good_attendance = ClassesTaken.objects.filter(user=user, times_present__gte=10)
        for class_ in classes_with_good_attendance:
            if CompletedCourses.objects.filter(course=class_.course).exists():
                continue
            ACTION_TO_CLASS[class_.course].process_exam(user)
        ClassesTaken.objects.filter(user=user).delete()

        user_data = UserData.objects.get(user=user)
        semester = user_data.semester()
        if semester == LAST_SEMESTER:
            return
        total_ects = sum(ACTION_TO_CLASS[class_.course].ects for class_ in CompletedCourses.objects.filter(user=user))
        failed = total_ects < ECTS_TO_PASS_SEMESTER * semester - (10 if semester != LAST_SEMESTER else 0)
        if failed:
            if user_data.failed_a_semester:
                CompletedCourses.objects.filter(user=user).delete()
                user_data.failed_a_semester = False
            else:
                user_data.failed_a_semester = True
            user_data.save()

        Message.objects.create(user=user, text=f'A semester has ended. You have {"failed" if failed else "passed"}!')


class Class(Action, ABC):
    ects: int
    semester: int
    abilities: tuple
    skills: tuple
    exam_factor: float

    @classmethod
    def process_exam(cls, user: User):
        user_data = UserData.objects.get(user=user)
        ability_bonuses = sum(values['exam_weight']
                              for ability, values in cls.abilities
                              if Abilities.objects.filter(user=user, ability=ability).exists())
        score = (uniform(0.75, 1.25)
                 * float(sum(getattr(user_data, skill) for skill, _ in cls.skills))
                 * cls.exam_factor
                 + ability_bonuses)
        passed = score >= SCORE_TO_PASS
        if passed:
            CompletedCourses.objects.create(user=user, course=cls.name)
        Message.objects.create(
            user=user,
            text=f'You have taken a(n) {cls.name} exam. You have {"passed!" if passed else "flunked :("}'
        )

    @classmethod
    @energy_decorator
    def process_action(cls, user: User):
        class_, _ = ClassesTaken.objects.get_or_create(user=user, course=cls.name)
        class_.times_present = F('times_present') + 1
        class_.save()

        user_data = UserData.objects.get(user=user)
        stats_before_action = get_state_before_action(user_data)
        for skill, values in cls.skills:
            gain = (values['random_factor']()
                    * get_mood_factor(user_data.mood)
                    / max(user_data.semester() + 1 - cls.semester, 1)
                    / (2 if getattr(user_data, skill) > values['threshold'] else 1))
            setattr(user_data, skill, Least(F(skill) + gain, 100))
        user_data.mood = Least(Greatest(F('mood') + uniform(-1.5, 0.5), 0), 100)
        user_data.energy = Greatest(F('energy') + uniform(-1.0, -0.1), 0)
        user_data.save()

        Message.objects.create(user=user, text=get_message(
            user_data, stats_before_action, f'attended {cls.name} class'
        ))
        for ability, values in cls.abilities:
            if random() < values['chance']:
                instance, created = Abilities.objects.get_or_create(user=user, ability=ability)
                if created:
                    Message.objects.create(user=user, text=f'You have earned a new ability: {ability}.')


# I SEMESTER

class Logic(Class):
    name = 'Logic'
    time = 8,
    ects = 8
    semester = 1
    abilities = ('Logic', {'chance': 0.15, 'exam_weight': 30}),
    skills = ('math', {'random_factor': lambda: uniform(0.3, 0.35), 'threshold': 25}),
    exam_factor = 4.1


class CalculusI(Class):
    name = 'Calculus I'
    time = 12,
    ects = 10
    semester = 1
    abilities = (('Basic Calculus', {'chance': 0.15, 'exam_weight': 20}),
                 ('Intermediate Calculus', {'chance': 0.01, 'exam_weight': 50}))
    skills = ('math', {'random_factor': lambda: uniform(0.3, 0.35), 'threshold': 20}),
    exam_factor = 4.7


class IntroToProgrammingPython(Class):
    name = 'Intro To Programming - Python'
    time = 9,
    ects = 6
    semester = 1
    abilities = (('Structured Programming', {'chance': 0.15, 'exam_weight': 15}),
                 ('Python Programming', {'chance': 0.15, 'exam_weight': 20}),
                 ('Object Oriented Programming', {'chance': 0.05, 'exam_weight': 15}))
    skills = ('programming', {'random_factor': lambda: uniform(0.3, 0.35), 'threshold': 20}),
    exam_factor = 6.2


class IntroToProgrammingC(Class):
    name = 'Intro To Programming - C'
    time = 9,
    ects = 6
    semester = 1
    abilities = (('Structured Programming', {'chance': 0.20, 'exam_weight': 15}),
                 ('C Programming', {'chance': 0.20, 'exam_weight': 30}),)
    skills = ('programming', {'random_factor': lambda: uniform(0.3, 0.35), 'threshold': 25}),
    exam_factor = 6.0


class IntroToCS(Class):
    name = 'Introduction To Computer Science'
    time = 13,
    ects = 6
    semester = 1
    abilities = ('Basic Algorithms', {'chance': 0.15, 'exam_weight': 15}),
    skills = (('programming', {'random_factor': lambda: uniform(0.15, 0.2), 'threshold': 20}),
              ('math', {'random_factor': lambda: uniform(0.15, 0.2), 'threshold': 20}))
    exam_factor = 3.2


# II SEMESTER

class Programming(Class):
    name = 'Programming'
    time = 11,
    ects = 9
    semester = 2
    abilities = ('Functional Programming', {'chance': 0.15, 'exam_weight': 25}),
    skills = ('programming', {'random_factor': lambda: uniform(0.4, 0.45), 'threshold': 40}),
    exam_factor = 2.4


class Algebra(Class):
    name = 'Algebra'
    time = 16,
    ects = 7
    semester = 2
    abilities = ('Algebra', {'chance': 0.15, 'exam_weight': 25}),
    skills = ('math', {'random_factor': lambda: uniform(0.25, 0.35), 'threshold': 35}),
    exam_factor = 2.7


class CppProgramming(Class):
    name = 'C++ Programming'
    time = 8,
    ects = 6
    semester = 2
    abilities = (('C++ Programming', {'chance': 0.15, 'exam_weight': 25}),
                 ('Object Oriented Programming', {'chance': 0.1, 'exam_weight': 15}))
    skills = ('programming', {'random_factor': lambda: uniform(0.25, 0.35), 'threshold': 35}),
    exam_factor = 2.9


class OOP(Class):
    name = 'Object Oriented Programming'
    time = 10,
    ects = 6
    semester = 2
    abilities = ('Object Oriented Programming', {'chance': 0.2, 'exam_weight': 25}),
    skills = ('programming', {'random_factor': lambda: uniform(0.3, 0.35), 'threshold': 35}),
    exam_factor = 2.9


class ComputerSystemsArchitectures(Class):
    name = 'Computer Systems Architectures'
    time = 15,
    ects = 6
    semester = 2
    abilities = ('Computer Architecture', {'chance': 0.2, 'exam_weight': 25}),
    skills = ('programming', {'random_factor': lambda: uniform(0.2, 0.3), 'threshold': 35}),
    exam_factor = 2.8


# III SEMESTER

class NumericalAnalysis(Class):
    name = 'Numerical Analysis'
    time = 13,
    ects = 10
    semester = 3
    abilities = (('Basic Numerical Analysis', {'chance': 0.15, 'exam_weight': 20}),
                 ('Intermediate Numerical Analysis', {'chance': 0.02, 'exam_weight': 35}))
    skills = (('programming', {'random_factor': lambda: uniform(0.1, 0.15), 'threshold': 55}),
              ('math', {'random_factor': lambda: uniform(0.1, 0.15), 'threshold': 55}))
    exam_factor = 0.9


class DiscreteMath(Class):
    name = 'Discrete Math'
    time = 16,
    ects = 8
    semester = 3
    abilities = (('Basic Discrete Math', {'chance': 0.15, 'exam_weight': 20}),
                 ('Intermediate Discrete Math', {'chance': 0.02, 'exam_weight': 35}),
                 ('Graph Algorithms', {'chance': 0.05, 'exam_weight': 10}))
    skills = ('math', {'random_factor': lambda: uniform(0.2, 0.25), 'threshold': 55}),
    exam_factor = 1.3


class Probability(Class):
    name = 'Probability'
    time = 12,
    ects = 6
    semester = 3
    abilities = ('Probability', {'chance': 0.15, 'exam_weight': 25}),
    skills = ('math', {'random_factor': lambda: uniform(0.2, 0.25), 'threshold': 55}),
    exam_factor = 2.0


class JavaProgramming(Class):
    name = 'Java Programming'
    time = 8,
    ects = 6
    semester = 3
    abilities = (('Java Programming', {'chance': 0.15, 'exam_weight': 20}),
                 ('Object Oriented Programming', {'chance': 0.1, 'exam_weight': 15}))
    skills = ('programming', {'random_factor': lambda: uniform(0.15, 0.2), 'threshold': 55}),
    exam_factor = 2.2


class PythonProgramming(Class):
    name = 'Python Programming'
    time = 10,
    ects = 6
    semester = 3
    abilities = (('Python Programming', {'chance': 0.15, 'exam_weight': 15}),
                 ('Object Oriented Programming', {'chance': 0.1, 'exam_weight': 10}),
                 ('Structured Programming', {'chance': 0.1, 'exam_weight': 10}))
    skills = ('programming', {'random_factor': lambda: uniform(0.15, 0.2), 'threshold': 55}),
    exam_factor = 2.2


class FunctionalProgramming(Class):
    name = 'Functional Programming'
    time = 17,
    ects = 6
    semester = 3
    abilities = ('Functional Programming', {'chance': 0.15, 'exam_weight': 25}),
    skills = (('programming', {'random_factor': lambda: uniform(0.1, 0.15), 'threshold': 55}),
              ('math', {'random_factor': lambda: uniform(0.05, 0.1), 'threshold': 55}))
    exam_factor = 1.1


# IV SEMESTER

class AlgorithmsAndDataStructures(Class):
    name = 'Algorithms And Data Structures'
    time = 14,
    ects = 10
    semester = 4
    abilities = (('Basic Algorithms', {'chance': 0.15, 'exam_weight': 10}),
                 ('Basic Data Structures', {'chance': 0.15, 'exam_weight': 10}),
                 ('Dynamic Programming', {'chance': 0.10, 'exam_weight': 5}),
                 ('Greedy Algorithms', {'chance': 0.10, 'exam_weight': 5}),
                 ('Graph Algorithms', {'chance': 0.05, 'exam_weight': 5}),
                 ('Intermediate Data Structures', {'chance': 0.02, 'exam_weight': 20}),
                 ('Intermediate Algorithms', {'chance': 0.02, 'exam_weight': 20}))
    skills = (('programming', {'random_factor': lambda: uniform(0.1, 0.15), 'threshold': 70}),
              ('algorithms', {'random_factor': lambda: uniform(0.3, 0.5), 'threshold': 85}),
              ('math', {'random_factor': lambda: uniform(0.05, 0.1), 'threshold': 70}))
    exam_factor = 0.35


class LinuxAdministration(Class):
    name = 'Linux Administration'
    time = 18,
    ects = 6
    semester = 4
    abilities = (('Linux Basics', {'chance': 0.15, 'exam_weight': 10}),
                 ('Linux Administration', {'chance': 0.05, 'exam_weight': 20}))
    skills = ('programming', {'random_factor': lambda: uniform(0.1, 0.15), 'threshold': 70}),
    exam_factor = 1.8


class ScalaProgramming(Class):
    name = 'Scala Programming'
    time = 16,
    ects = 6
    semester = 4
    abilities = (('Scala Programming', {'chance': 0.15, 'exam_weight': 20}),
                 ('Functional Programming', {'chance': 0.15, 'exam_weight': 10}))
    skills = ('programming', {'random_factor': lambda: uniform(0.1, 0.15), 'threshold': 70}),
    exam_factor = 1.6


class LambdaCalculus(Class):
    name = 'Lambda Calculus'
    time = 13,
    ects = 6
    semester = 4
    abilities = ('Lambda Calculus', {'chance': 0.15, 'exam_weight': 25}),
    skills = ('math', {'random_factor': lambda: uniform(0.1, 0.15), 'threshold': 70}),
    exam_factor = 1.7


class CalculusII(Class):
    name = 'Calculus II'
    time = 9,
    ects = 6
    semester = 4
    abilities = (('Basic Calculus', {'chance': 0.5, 'exam_weight': 10}),
                 ('Intermediate Calculus', {'chance': 0.15, 'exam_weight': 20}))
    skills = ('math', {'random_factor': lambda: uniform(0.1, 0.15), 'threshold': 70}),
    exam_factor = 1.6


# V SEMESTER

class OperatingSystems(Class):
    name = 'Operating Systems'
    time = 15,
    ects = 6
    semester = 5
    abilities = (('Operating Systems', {'chance': 0.15, 'exam_weight': 15}),
                 ('Computer Architecture', {'chance': 0.15, 'exam_weight': 10}))
    skills = ('programming', {'random_factor': lambda: uniform(0.1, 0.15), 'threshold': 90}),
    exam_factor = 1.3


class RustProgramming(Class):
    name = 'Rust Programming'
    time = 14,
    ects = 6
    semester = 5
    abilities = (('Rust Programming', {'chance': 0.15, 'exam_weight': 15}),
                 ('Structured Programming', {'chance': 0.15, 'exam_weight': 5}),
                 ('Object Oriented Programming', {'chance': 0.15, 'exam_weight': 5}),
                 ('Functional Programming', {'chance': 0.15, 'exam_weight': 5}))
    skills = ('programming', {'random_factor': lambda: uniform(0.1, 0.15), 'threshold': 90}),
    exam_factor = 1.5


class SoftwareEngineering(Class):
    name = 'Software Engineering'
    time = 11,
    ects = 6
    semester = 5
    abilities = ('Software Engineering', {'chance': 0.15, 'exam_weight': 25}),
    skills = ('work_experience', {'random_factor': lambda: uniform(0.1, 0.15), 'threshold': 100}),
    exam_factor = 2.5


class MachineLearning(Class):
    name = 'Machine Learning'
    time = 10,
    ects = 6
    semester = 5
    abilities = ('Machine Learning', {'chance': 0.15, 'exam_weight': 25}),
    skills = (('algorithms', {'random_factor': lambda: uniform(0.05, 0.1), 'threshold': 90}),
              ('programming', {'random_factor': lambda: uniform(0.05, 0.1), 'threshold': 90}),
              ('math', {'random_factor': lambda: uniform(0.05, 0.1), 'threshold': 90}))
    exam_factor = 0.55


class EmbeddedSystems(Class):
    name = 'Embedded Systems'
    time = 18,
    ects = 6
    semester = 5
    abilities = ('Embedded Programming', {'chance': 0.15, 'exam_weight': 25}),
    skills = ('programming', {'random_factor': lambda: uniform(0.1, 0.15), 'threshold': 90}),
    exam_factor = 1.5


# VI SEMESTER

class Databases(Class):
    name = 'Databases'
    time = 14,
    ects = 6
    semester = 6
    abilities = ('Databases', {'chance': 0.15, 'exam_weight': 25}),
    skills = (('programming', {'random_factor': lambda: uniform(0.05, 0.1), 'threshold': 100}),
              ('math', {'random_factor': lambda: uniform(0.05, 0.1), 'threshold': 100}))
    exam_factor = 0.75


class ComputerNetworks(Class):
    name = 'Computer Networks'
    time = 12,
    ects = 6
    semester = 6
    abilities = ('Computer Networks', {'chance': 0.15, 'exam_weight': 25}),
    skills = (('programming', {'random_factor': lambda: uniform(0.05, 0.1), 'threshold': 100}),
              ('math', {'random_factor': lambda: uniform(0.05, 0.1), 'threshold': 100}))
    exam_factor = 0.65


class JFIZO(Class):
    name = 'JFIZO'
    time = 7,
    ects = 12
    semester = 6
    abilities = ('JFIZO', {'chance': 0.1, 'exam_weight': 25}),
    skills = (('programming', {'random_factor': lambda: uniform(0.1, 0.15), 'threshold': 100}),
              ('math', {'random_factor': lambda: uniform(0.1, 0.15), 'threshold': 100}),
              ('algorithms', {'random_factor': lambda: uniform(0.1, 0.15), 'threshold': 100}))
    exam_factor = 0.3


class ArtificialIntelligence(Class):
    name = 'Artificial Intelligence'
    time = 17,
    ects = 6
    semester = 6
    abilities = ('Artificial Intelligence', {'chance': 0.15, 'exam_weight': 25}),
    skills = (('programming', {'random_factor': lambda: uniform(0.05, 0.1), 'threshold': 100}),
              ('math', {'random_factor': lambda: uniform(0.05, 0.1), 'threshold': 100}))
    exam_factor = 0.55


ACTION_TO_CLASS = {
    class_.name: class_ for class_ in [
        Sleep, Work, LearnMath, LearnProgramming, LearnAlgorithms, Relax, Party, FinishSemester, EndDay,
        Logic, CalculusI, IntroToProgrammingPython, IntroToProgrammingC, IntroToCS, Programming, Algebra,
        CppProgramming, OOP, ComputerSystemsArchitectures, NumericalAnalysis, DiscreteMath, Probability,
        JavaProgramming, PythonProgramming, FunctionalProgramming, AlgorithmsAndDataStructures, LinuxAdministration,
        ScalaProgramming, LambdaCalculus, CalculusII, OperatingSystems, RustProgramming, SoftwareEngineering,
        MachineLearning, EmbeddedSystems, Databases, ComputerNetworks, JFIZO, ArtificialIntelligence
    ]
}
