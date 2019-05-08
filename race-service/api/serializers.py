from rest_framework import serializers
from api.models import Race


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
