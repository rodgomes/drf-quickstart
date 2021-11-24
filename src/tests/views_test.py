from django.urls import reverse
from django.utils import timezone

import pytest

from api.models import Person


@pytest.mark.django_db
class TestPersonViewSet:
    def test_create_person(self, authenticated_client):
        data = {"name": "My Friend", "birthdate": "09-09-1999", "phone": "+31600000000", "email": "test@example.com"}
        resp = authenticated_client.post(reverse("api:persons-list"), data=data)
        assert resp.status_code == 201

    def test_create_missing_name(self, authenticated_client):
        data = {"birthdate": "09-09-1999"}
        resp = authenticated_client.post(reverse("api:persons-list"), data=data)
        assert resp.status_code == 400
        response_dict = resp.json()
        assert response_dict["name"][0] == "This field is required."

    def test_create_invalid_date(self, authenticated_client):
        data = {"name": "test", "birthdate": "34-09-1999"}
        resp = authenticated_client.post(reverse("api:persons-list"), data=data)
        assert resp.status_code == 400
        response_dict = resp.json()
        assert response_dict["birthdate"][0] == "Date has wrong format. Use one of these formats instead: DD-MM-YYYY."

    def test_create_missing_birthdate(self, authenticated_client):
        data = {"name": "test"}
        resp = authenticated_client.post(reverse("api:persons-list"), data=data)
        assert resp.status_code == 400
        response_dict = resp.json()
        assert response_dict["birthdate"][0] == "This field is required."

    def test_create_missing_all_required(self, authenticated_client):
        data = {}
        resp = authenticated_client.post(reverse("api:persons-list"), data=data)
        assert resp.status_code == 400
        response_dict = resp.json()
        assert response_dict["birthdate"][0] == "This field is required."
        assert response_dict["name"][0] == "This field is required."

    def test_list_all(self, authenticated_client, user):
        Person.objects.create(name="Test1", birthdate=timezone.now(), user=user)
        Person.objects.create(name="Test2", birthdate=timezone.now(), user=user)
        resp = authenticated_client.get(reverse("api:persons-list"))
        assert resp.status_code == 200
        response_dict = resp.json()
        assert len(response_dict) == 2
        names = [d["name"] for d in response_dict]
        assert "Test1" in names
        assert "Test2" in names

    def test_get_person(self, authenticated_client, user):
        p1 = Person.objects.create(name="Test1", birthdate=timezone.now(), user=user)
        resp = authenticated_client.get(reverse("api:persons-detail", kwargs={"pk": p1.pk}))
        assert resp.status_code == 200
        response_dict = resp.json()
        assert response_dict["name"] == "Test1"

    def test_get_only_my_person(self, authenticated_client, another_user):
        p1 = Person.objects.create(name="Test1", birthdate=timezone.now(), user=another_user)
        resp = authenticated_client.get(reverse("api:persons-detail", kwargs={"pk": p1.pk}))
        assert resp.status_code == 404

    def test_get_non_existing_person(self, authenticated_client):
        resp = authenticated_client.get(reverse("api:persons-detail", kwargs={"pk": "non-existing"}))
        assert resp.status_code == 404

    def test_change_persons_name(self, authenticated_client, user):
        p1 = Person.objects.create(name="Test1", birthdate=timezone.now(), user=user)
        resp = authenticated_client.get(reverse("api:persons-detail", kwargs={"pk": p1.pk}))
        response_dict = resp.json()
        assert response_dict["name"] == "Test1"
        data = {"name": "New name"}
        resp = authenticated_client.patch(
            reverse("api:persons-detail", kwargs={"pk": p1.pk}), data=data, content_type="application/json"
        )
        assert resp.status_code == 200
        resp = authenticated_client.get(reverse("api:persons-detail", kwargs={"pk": p1.pk}))
        response_dict = resp.json()
        assert response_dict["name"] == "New name"

    def test_delete_person(self, authenticated_client, user):
        p1 = Person.objects.create(name="Test1", birthdate=timezone.now(), user=user)
        resp = authenticated_client.delete(reverse("api:persons-detail", kwargs={"pk": p1.pk}))
        assert resp.status_code == 204
        resp = authenticated_client.get(reverse("api:persons-detail", kwargs={"pk": p1.pk}))
        assert resp.status_code == 404


@pytest.mark.django_db
class TestReminderViewSet:
    def test_create_reminder(self, authenticated_client, test_person):
        data = {"birthday_person": test_person.pk, "how_early": 10}
        resp = authenticated_client.post(reverse("api:reminders-list"), data=data)
        assert resp.status_code == 201

    def test_create_reminder_from_people_on_your_list(self, authenticated_client, test_another_person):
        data = {"birthday_person": test_another_person.pk}
        resp = authenticated_client.post(reverse("api:reminders-list"), data=data)
        assert resp.status_code == 400
        response_dict = resp.json()
        assert response_dict["birthday_person"][0] == 'Invalid pk "2" - object does not exist.'

    def test_create_reminder_from_non_existing_person(self, authenticated_client):
        data = {"birthday_person": 99}
        resp = authenticated_client.post(reverse("api:reminders-list"), data=data)
        assert resp.status_code == 400
        response_dict = resp.json()
        assert response_dict["birthday_person"][0] == 'Invalid pk "99" - object does not exist.'

    def test_list_only_my_contacts(self, authenticated_client, user, test_another_reminder, test_reminder):
        resp = authenticated_client.get(reverse("api:reminders-list"))
        assert resp.status_code == 200
        response_dict = resp.json()
        assert len(response_dict) == 1
        assert response_dict[0]["birthday_person"] == test_reminder.birthday_person.pk
