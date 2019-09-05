from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from api.models import Race, RaceResult, RaceGroup


class RaceSerializer(serializers.ModelSerializer):
    race_results_url = serializers.HyperlinkedIdentityField(
        read_only=True,
        view_name="api:race-results-list",
        lookup_field="pk",
        lookup_url_kwarg="parent_lookup_race",
    )

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
            "race_results_url",
            "itra_race_id",
        )
        read_only_field = ("id", "elevation_diff", "race_results_url")
        # read_only_field = ("id", "elevation_diff")


class RaceGroupSerializer(serializers.ModelSerializer):
    races = RaceSerializer(many=True, read_only=True)

    class Meta:

        model = RaceGroup
        fields = ("id", "name", "races")


class RaceResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = RaceResult
        fields = (
            "id",
            "race",
            "runner_name",
            "runner_birth",
            "time_result",
            "sex",
        )
        read_only_field = ("id", "race")
        validators = [
            UniqueTogetherValidator(
                queryset=RaceResult.objects.all(),
                fields=("race", "runner_name", "runner_birth", "time_result"),
            )
        ]
