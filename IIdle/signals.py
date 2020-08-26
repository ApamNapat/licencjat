from django.contrib.auth.models import User
from django.db.models.signals import post_save

from IIdle.models import UserData


def create_user_data(sender, instance: User, created: bool, **kwargs):
    if created:
        UserData.objects.create(user=instance)


post_save.connect(receiver=create_user_data, sender=User, weak=False, dispatch_uid='User data handler')
