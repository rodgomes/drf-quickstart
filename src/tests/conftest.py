from django.contrib.auth import get_user_model
from django.utils import timezone
from api.models import Person

import pytest


@pytest.fixture
def user():
    username = "user1"
    password = "fakepass"
    return get_user_model().objects.create_user(username=username, password=password)


@pytest.fixture
def test_person(user):
    return Person.objects.create(name="Test1", birthdate=timezone.now(), user=user)


@pytest.fixture
def authenticated_client(client, user):
    client.force_login(user)
    return client
