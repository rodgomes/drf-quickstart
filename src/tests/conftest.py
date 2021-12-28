from datetime import datetime

from django.contrib.auth import get_user_model
from django.utils import timezone

import pytest

from api.models import Person, Reminder


@pytest.fixture
def user():
    username = "user1"
    password = "fakepass"
    return get_user_model().objects.create_user(username=username, password=password, email="test@example.com")


@pytest.fixture
def another_user():
    username = "user2"
    password = "fakepass"
    return get_user_model().objects.create_user(username=username, password=password, email="test2@example.com")


@pytest.fixture
def test_person(user):
    bday = datetime.strptime("09-09-1999", "%d-%m-%Y")
    return Person.objects.create(name="Test1", birthdate=bday, user=user)


@pytest.fixture
def test_another_person(another_user):
    return Person.objects.create(name="Test1", birthdate=timezone.now(), user=another_user)


@pytest.fixture
def test_another_reminder(test_another_person):
    return Reminder.objects.create(birthday_person=test_another_person)


@pytest.fixture
def test_reminder(test_person):
    return Reminder.objects.create(birthday_person=test_person, reminder_day=test_person.birthdate)


@pytest.fixture
def test_reminder_with_no_email(test_person):
    test_person.user.email = ""
    test_person.user.save()
    return Reminder.objects.create(birthday_person=test_person, reminder_day=test_person.birthdate)


@pytest.fixture
def authenticated_client(client, user):
    client.force_login(user)
    return client
