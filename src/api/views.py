from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api.models import Person, Reminder
from api.serializers import PersonSerializer, ReminderSerializer


class ReminderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ReminderSerializer

    def get_queryset(self):
        # ensure you get only your own reminders
        return Reminder.objects.filter(birthday_person__user=self.request.user.pk)


class PersonViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
