from django.contrib import admin

from IIdle.models import UserData, Abilities, Timetable, CompletedCourses, ClassesTaken, Message


class UserDataAdmin(admin.ModelAdmin):
    list_display = ('user',)


class AbilitiesAdmin(admin.ModelAdmin):
    list_display = ('user',)


class TimetableDataAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'time')


admin.site.register(UserData, UserDataAdmin)
admin.site.register(Abilities, AbilitiesAdmin)
admin.site.register(Timetable, TimetableDataAdmin)
admin.site.register(CompletedCourses)
admin.site.register(ClassesTaken)
admin.site.register(Message)
