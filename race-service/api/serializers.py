from rest_framework import serializers
from api.models import Race, RaceResult


class RaceSerializer(serializers.ModelSerializer):
    """Serializer for race objects"""

    class Meta:
        model = Race
        fields = (
            "id",
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


class RaceResultSerializer(serializers.ModelSerializer):
    """Serializer for race_result objects"""

    class Meta:
        model = RaceResult
        fields = ("id", "runner_name", "runner_birth", "time_result")
        read_only_field = ("id",)
