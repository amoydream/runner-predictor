from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from api.models import Runner, RaceResult
from django.core.exceptions import ValidationError


class RunnerSerializer(serializers.ModelSerializer):
    """Serializer for runner objects"""

    birth_year = serializers.IntegerField()

    class Meta:
        model = Runner
        fields = ("id", "name", "birth_year")
        read_only_field = ("id",)

    def create(self, validated_data):
        runner = Runner(**validated_data)
        try:
            runner.save()
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return runner


class RaceResultSerializer(serializers.ModelSerializer):
    """Serializer for race_result objects"""

    class Meta:
        model = RaceResult
        fields = ("id", "race", "runner_name", "runner_birth", "time_result")
        read_only_field = ("id", "runner")
        validators = [
            UniqueTogetherValidator(
                queryset=RaceResult.objects.all(),
                fields=("runner", "event_name", "race_date"),
            )
        ]
