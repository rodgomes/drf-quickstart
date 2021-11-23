from django.contrib.auth import get_user_model
from django.db import models


class AuditMixin:
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Person(models.Model, AuditMixin):

    name = models.CharField(max_length=256)
    birthdate = models.DateField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    email = models.EmailField(null=True)
    phone = models.CharField(max_length=100, null=True)


class Reminder(models.Model, AuditMixin):

    birthday_person = models.OneToOneField(Person, on_delete=models.CASCADE)
    how_early = models.PositiveIntegerField(default=0)
