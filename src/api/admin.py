from django.contrib import admin

from api.models import Person, Reminder


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    pass


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    pass
