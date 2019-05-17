from rest_framework import viewsets
from api import serializers
from rest_framework_extensions.mixins import NestedViewSetMixin
from api.models import Race, RaceResult
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist


class RaceViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """Manage Race in the database"""

    queryset = Race.objects.all()
    serializer_class = serializers.RaceSerializer


class RaceResultViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """Manage RaceResult in the database"""

    queryset = RaceResult.objects.all()
    serializer_class = serializers.RaceResultSerializer

    def perform_create(self, serializer):
        """Create a new object"""
        race_id = self.kwargs.get("parent_lookup_race")
        try:
            race = Race.objects.get(pk=race_id)
        except ObjectDoesNotExist:
            raise ValidationError("Race dosen't Exists")
        serializer.save(race=race)
