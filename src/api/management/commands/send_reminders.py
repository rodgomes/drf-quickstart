import logging
from datetime import datetime

from django.conf import settings
from django.core.mail import send_mail
from django.core.management import BaseCommand

from api.models import Reminder

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    help = "Send reminder to all users about upcoming birhdays"

    def handle(self, *args, **options):
        today = datetime.now().date()
        logger.info(f"Sending reminders for date {today}")
        reminders_for_today = Reminder.objects.filter(
            reminder_day__day=today.day, reminder_day__month=today.month
        ).select_related()
        if not reminders_for_today:
            logger.info("No reminders to send today.")
            return
        for reminder in reminders_for_today:
            user = reminder.birthday_person.user
            if user.email:
                subject, message = self._get_subject_and_message(reminder)
                try:
                    logger.debug(f"Sending reminder to {user.email}")
                    send_mail(
                        f"Reminder: {subject}",
                        f"{message}",
                        settings.DEFAULT_EMAIL_FROM,
                        [user.email],
                        fail_silently=False,
                    )
                except Exception as e:
                    logger.exception(f"Could not send email to {user.email}: {e}")
            else:
                logger.warning(f"Could not send a reminder to user {user.pk}: missing email address.")
        logger.info(f"Finished sending reminders for date {today}")

    def _get_subject_and_message(self, reminder):
        subject_content = ""
        message = ""
        bday_is_today = reminder.how_early == 0

        if bday_is_today:
            subject_content = f"today is {reminder.birthday_person.name} birthday!"
            message = f"Take this moment to congratulate {reminder.birthday_person.name}"
        else:
            subject_content = f"in {reminder.how_early} day(s) is {reminder.birthday_person.name}'s birthday!"
            message = "Maybe you wanna buy a gift or prepare a nice surprise?"
        return subject_content, message
