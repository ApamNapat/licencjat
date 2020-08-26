from django.contrib.auth.models import User
from django.test import TestCase

from IIdle.models import UserData


class UserDataAndSemesterEndAdded(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='abc')
        self.user2 = User.objects.create(username='xyz')

    def test_user_data_created(self):
        first = UserData.objects.get(user__username='abc')
        second = UserData.objects.get(user__username='xyz')
        self.assertTrue(first.cash == second.cash == 500)
        self.assertTrue(first.energy == second.energy == 50)
        self.assertTrue(first.mood == second.mood == 50)
