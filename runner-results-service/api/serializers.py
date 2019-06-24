from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api.models import Runner, RaceResult
from django.core.exceptions import ValidationError


class RunnerSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for runner objects"""

    birth_year = serializers.IntegerField()
    url = serializers.HyperlinkedIdentityField(
        read_only=True, view_name="api:runner-detail"
    )

    class Meta:
        model = Runner
        fields = ("id", "name", "sex", "birth_year", "url")
        read_only_field = ("id", "url")

    def create(self, validated_data):
        runner = Runner(**validated_data)
        try:
            runner.save()
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return runner


class RunnerDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed view runner objects"""

    race_results = serializers.StringRelatedField(many=True)

    class Meta:
        model = Runner
        fields = ("id", "name", "sex", "birth_year", "race_results")
        read_only_field = ("id", "race_results")


class RaceResultSerializer(serializers.ModelSerializer):
    """Serializer for race_result objects"""

    distance = serializers.CharField(max_length=10)

    class Meta:
        model = RaceResult
        fields = (
            "id",
            "runner",
            "event_name",
            "distance",
            "race_date",
            "result_of_the_race",
            "race_type",
        )
        read_only_field = ("id", "runner")
        validators = [
            UniqueTogetherValidator(
                queryset=RaceResult.objects.all(),
                fields=("runner", "event_name", "race_date"),
            )
        ]
