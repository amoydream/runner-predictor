from rest_framework import viewsets
from api import serializers
from api.models import Race


class RaceViewSet(viewsets.ModelViewSet):
    """Manage Race in the database"""

    queryset = Race.objects.all()
    serializer_class = serializers.RaceSerializer
