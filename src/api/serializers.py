from rest_framework import exceptions, serializers

from api.models import Person, Reminder


class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        fields = ("birthday_person", "how_early")
        read_only_fields = ("created", "updated")

    def validate_birthday_person(self, person):
        if self.context["request"].user.pk != person.user.pk:
            # error message to be consistent with DRF default error message
            raise exceptions.ValidationError(f'Invalid pk "{person.user.pk}" - object does not exist.')
        return person


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
