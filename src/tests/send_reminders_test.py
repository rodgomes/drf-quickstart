from django.core.management import call_command

import pytest


@pytest.mark.django_db
class TestSendRemindersCommand:
    def test_send_reminder_nothing_to_send(self, caplog):
        call_command("send_reminders")
        assert "No reminders to send today." in caplog.text

    @pytest.mark.freeze_time("2021-09-09")
    def test_send_reminder(self, caplog, test_reminder):
        call_command("send_reminders")
        assert "Sending reminder to test@example.com" in caplog.text

    @pytest.mark.freeze_time("2021-09-09")
    def test_send_reminder_no_email_found(self, caplog, test_reminder_with_no_email):
        call_command("send_reminders")
        user_id = test_reminder_with_no_email.birthday_person.user.pk
        assert f"Could not send a reminder to user {user_id}: missing email address." in caplog.text
