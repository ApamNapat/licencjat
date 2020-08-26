from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from IIdle.api.serializers import (UserDataSerializer, TimetableSerializer, AbilitiesSerializer,
                                   CompletedCoursesSerializer, ClassesTakenSerializer, MessageSerializer)
from IIdle.models import UserData, Timetable, Abilities, CompletedCourses, ClassesTaken, Message

from IIdle.timetable_processor import validate_and_process_timetable_change, list_valid_actions, process_timetable


class UserDataDetails(APIView):
    def get(self, request, pk):
        process_timetable_wrapper(pk)
        try:
            user_data = UserData.objects.get(user_id=pk)
        except UserData.DoesNotExist:
            return Response({})
        serializer = UserDataSerializer(user_data)
        return Response(serializer.data)


class TimetableForUser(APIView):
    def get(self, request, pk):
        process_timetable_wrapper(pk)
        timetables = Timetable.objects.filter(user_id=pk)
        serializer = TimetableSerializer(timetables, many=True)
        return Response(serializer.data)


class CompletedCoursesForUser(APIView):
    def get(self, request, pk):
        process_timetable_wrapper(pk)
        completed_courses = CompletedCourses.objects.filter(user_id=pk)
        serializer = CompletedCoursesSerializer(completed_courses, many=True)
        return Response(serializer.data)


class ClassesTakenForUser(APIView):
    def get(self, request, pk):
        process_timetable_wrapper(pk)
        classes_taken = ClassesTaken.objects.filter(user_id=pk)
        serializer = ClassesTakenSerializer(classes_taken, many=True)
        return Response(serializer.data)


class AbilitiesForUser(APIView):
    def get(self, request, pk):
        process_timetable_wrapper(pk)
        abilities = Abilities.objects.filter(user_id=pk)
        serializer = AbilitiesSerializer(abilities, many=True)
        return Response(serializer.data)


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user == User.objects.get(pk=view.kwargs['pk'])


class SetTimetable(APIView):
    permission_classes = [IsAuthenticated & IsOwner]

    def post(self, request, pk):
        process_timetable_wrapper(pk)
        success, message = validate_and_process_timetable_change(User.objects.get(pk=pk), request.data)
        return Response({'success': success, 'message': message})


class GetValidActions(APIView):
    permission_classes = [IsAuthenticated & IsOwner]

    def get(self, request, pk):
        process_timetable_wrapper(pk)
        valid_actions = list_valid_actions(User.objects.get(pk=pk))
        return Response(valid_actions)


class ClearMessages(APIView):
    permission_classes = [IsAuthenticated & IsOwner]

    def post(self, request, pk):
        # process_timetable_wrapper should not be called
        Message.objects.filter(user_id=pk).delete()
        return Response({'success': True})


class MessagesForUser(APIView):
    permission_classes = [IsAuthenticated & IsOwner]

    def get(self, request, pk):
        process_timetable_wrapper(pk)
        messages = Message.objects.filter(user_id=pk)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


class CustomAuthToken(ObtainAuthToken):
    # Based on an example from docs
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'pk': user.pk,
        })


def process_timetable_wrapper(pk: int):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return
    process_timetable(user)
