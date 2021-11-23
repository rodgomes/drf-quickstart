from rest_framework import serializers

from api.models import Person, Reminder


class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        fields = ("birthday_person", "how_early")
        read_only_fields = ("created", "updated")


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
