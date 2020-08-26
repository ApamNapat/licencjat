from django.contrib.auth.models import User
from rest_framework import serializers

from IIdle.actions import ACTION_TO_CLASS
from IIdle.models import UserData, Timetable, CompletedCourses, ClassesTaken, Abilities, Message


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'pk']


class UserDataSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    semester = serializers.SerializerMethodField()

    class Meta:
        model = UserData
        fields = '__all__'

    def get_semester(self, obj):
        return obj.semester()


class TimetableSerializer(serializers.ModelSerializer):
    hour = serializers.SerializerMethodField()

    class Meta:
        model = Timetable
        exclude = ('id', 'user')

    def get_hour(self, obj):
        return obj.user.data.hour


class CompletedCoursesSerializer(serializers.ModelSerializer):
    ects = serializers.SerializerMethodField()

    class Meta:
        model = CompletedCourses
        exclude = ('id', 'user')

    def get_ects(self, obj):
        return ACTION_TO_CLASS[obj.course].ects


class ClassesTakenSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassesTaken
        exclude = ('id', 'user')


class AbilitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Abilities
        exclude = ('id', 'user')


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        exclude = ('id', 'user', 'time')
