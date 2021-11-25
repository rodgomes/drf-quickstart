from datetime import timedelta

from rest_framework import exceptions, serializers

from api.models import Person, Reminder


class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        fields = ("birthday_person", "how_early")
        read_only_fields = ("reminder_day", "created", "updated")

    def validate_birthday_person(self, person):
        if self.context["request"].user.pk != person.user.pk:
            # error message to be consistent with DRF default error message
            raise exceptions.ValidationError(f'Invalid pk "{person.user.pk}" - object does not exist.')
        return person

    def create(self, validated_data):
        # in order to make it easy to get all reminders of the day, we save the date we should be reminded
        # as a `birthdate - how_early` simple calculation. The year in the date field is ignored.
        validated_data["reminder_day"] = validated_data["birthday_person"].birthdate - timedelta(
            days=validated_data["how_early"]
        )
        return super().create(validated_data)


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = (
            "name",
            "birthdate",
        )
        read_only_fields = ("user", "created", "updated")

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
