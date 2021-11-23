from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api.models import Person, Reminder
from api.serializers import PersonSerializer, ReminderSerializer


class ReminderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Reminder.objects.all()
    serializer_class = ReminderSerializer


class PersonViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
