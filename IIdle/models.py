from django.contrib.auth.models import User
from django.db.models import (
    OneToOneField, DecimalField, IntegerField, ForeignKey, CharField, Model, CASCADE, CheckConstraint, Q, BooleanField,
    DateTimeField, TextField
)

from IIdle.abilities import ABILITIES
from IIdle.consts import LAST_SEMESTER


class UserData(Model):
    user = OneToOneField(User, on_delete=CASCADE, related_name='data', primary_key=True)
    cash = DecimalField(max_digits=10, decimal_places=2, default=500)
    energy = DecimalField(max_digits=5, decimal_places=2, default=50)
    mood = DecimalField(max_digits=5, decimal_places=2, default=50)
    failed_a_semester = BooleanField(default=False)
    math = DecimalField(max_digits=5, decimal_places=2, default=0)
    programming = DecimalField(max_digits=5, decimal_places=2, default=0)
    algorithms = DecimalField(max_digits=5, decimal_places=2, default=0)
    work_experience = DecimalField(max_digits=5, decimal_places=2, default=0)
    day = IntegerField(default=0)
    hour = IntegerField(default=0)

    def semester(self):
        return max(min(self.day // 14 + (1 if not self.failed_a_semester else 0), LAST_SEMESTER), 1)

    class Meta:
        constraints = [
            CheckConstraint(check=Q(energy__lte=100, energy__gte=0), name='energy_range'),
            CheckConstraint(check=Q(mood__lte=100, mood__gte=0), name='mood_range'),
            CheckConstraint(check=Q(hour__lte=23, hour__gte=0), name='hour_range'),
            CheckConstraint(check=Q(day__gte=0), name='day_range'),
            CheckConstraint(check=Q(math__lte=100, math__gte=0), name='math_range'),
            CheckConstraint(check=Q(programming__lte=100, programming__gte=0), name='programming_range'),
            CheckConstraint(check=Q(algorithms__lte=100, algorithms__gte=0), name='algorithms_range'),
            CheckConstraint(check=Q(work_experience__lte=100, work_experience__gte=0), name='work_experience_range'),
        ]


CLASSES_CHOICES = {
    'Logic': 'Logic',
    'Calculus I': 'Calculus I',
    'Intro To Programming - Python': 'Intro To Programming - Python',
    'Intro To Programming - C': 'Intro To Programming - C',
    'Introduction To Computer Science': 'Introduction To Computer Science',
    'Programming': 'Programming',
    'Algebra': 'Algebra',
    'C++ Programming': 'C++ Programming',
    'Object Oriented Programming': 'Object Oriented Programming',
    'Computer Systems Architectures': 'Computer Systems Architectures',
    'Numerical Analysis': 'Numerical Analysis',
    'Discrete Math': 'Discrete Math',
    'Probability': 'Probability',
    'Java Programming': 'Java Programming',
    'Python Programming': 'Python Programming',
    'Functional Programming': 'Functional Programming',
    'Algorithms And Data Structures': 'Algorithms And Data Structures',
    'Linux Administration': 'Linux Administration',
    'Scala Programming': 'Scala Programming',
    'Lambda Calculus': 'Lambda Calculus',
    'Calculus II': 'Calculus II',
    'Operating Systems': 'Operating Systems',
    'Rust Programming': 'Rust Programming',
    'Software Engineering': 'Software Engineering',
    'Machine Learning': 'Machine Learning',
    'Embedded Systems': 'Embedded Systems',
    'Databases': 'Databases',
    'Computer Networks': 'Computer Networks',
    'JFIZO': 'JFIZO',
    'Artificial Intelligence': 'Artificial Intelligence',
}

ACTIONS_CHOICES = {
    'Sleep': 'Sleep',
    'Work': 'Work',
    'Learn Math': 'Learn Math',
    'Learn Programming': 'Learn Programming',
    'Learn Algorithms': 'Learn Algorithms',
    'Relax': 'Relax',
    'Party': 'Party',
    'Finish Semester': 'Finish Semester',
    'End Day': 'End Day',
    **CLASSES_CHOICES,
}


class Timetable(Model):
    user = ForeignKey(User, on_delete=CASCADE)
    action = CharField(max_length=50, choices=ACTIONS_CHOICES.items())
    time = DateTimeField()

    class Meta:
        ordering = ['time']

    def __str__(self):
        return f'{self.user.username} {self.action} {self.time.date()}'


class CompletedCourses(Model):
    user = ForeignKey(User, on_delete=CASCADE)
    course = CharField(max_length=50, choices=CLASSES_CHOICES.items())

    class Meta:
        unique_together = ['user', 'course']


class ClassesTaken(Model):
    user = ForeignKey(User, on_delete=CASCADE)
    course = CharField(max_length=50, choices=CLASSES_CHOICES.items())
    times_present = IntegerField(default=0)

    class Meta:
        unique_together = ['user', 'course']


class Abilities(Model):
    user = ForeignKey(User, on_delete=CASCADE)
    ability = CharField(max_length=40, choices=ABILITIES)

    class Meta:
        unique_together = ['user', 'ability']


class Message(Model):
    user = ForeignKey(User, on_delete=CASCADE)
    text = TextField()
    time = DateTimeField(auto_now=True)

    class Meta:
        ordering = ['time']
