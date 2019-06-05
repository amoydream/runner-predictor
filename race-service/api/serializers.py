from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from api.models import Race, RaceResult, RaceGroup


class RaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Race
        fields = (
            "id",
            "race_group",
            "name",
            "start_date",
            "distance",
            "elevation_gain",
            "elevation_lost",
            "itra",
            "food_point",
            "time_limit",
            "elevation_diff",
        )
        read_only_field = ("id", "elevation_diff")


class RaceGroupSerializer(serializers.ModelSerializer):
    races = serializers.HyperlinkedRelatedField(
        many=True, view_name="api:race-detail", read_only=True
    )

    class Meta:
        model = RaceGroup
        fields = ("id", "name", "races")
        read_only_field = ("id", "races")


class RaceResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = RaceResult
        fields = ("id", "race", "runner_name", "runner_birth", "time_result")
        read_only_field = ("id", "race")
        validators = [
            UniqueTogetherValidator(
                queryset=RaceResult.objects.all(),
                fields=("race", "runner_name", "runner_birth", "time_result"),
            )
        ]
