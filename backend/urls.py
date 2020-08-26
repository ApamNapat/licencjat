"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from IIdle.api.views import (UserDataDetails, TimetableForUser, CompletedCoursesForUser, ClassesTakenForUser,
                             AbilitiesForUser, SetTimetable, GetValidActions, CustomAuthToken, MessagesForUser,
                             ClearMessages)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('userdata/<int:pk>/', UserDataDetails.as_view()),
    path('timetable/<int:pk>/', TimetableForUser.as_view()),
    path('courses/<int:pk>/', CompletedCoursesForUser.as_view()),
    path('classes/<int:pk>/', ClassesTakenForUser.as_view()),
    path('abilities/<int:pk>/', AbilitiesForUser.as_view()),
    path('messages/<int:pk>/', MessagesForUser.as_view()),
    path('clearmessages/<int:pk>/', ClearMessages.as_view()),
    path('set_timetable/<int:pk>/', SetTimetable.as_view()),
    path('get_valid_actions/<int:pk>/', GetValidActions.as_view()),
    path('get_token/', CustomAuthToken.as_view()),
    path('authentication/', include('dj_rest_auth.urls')),
    path('authentication/registration/', include('dj_rest_auth.registration.urls')),
]
