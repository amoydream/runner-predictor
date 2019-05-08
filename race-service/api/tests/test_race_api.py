from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from api.models import Race
from api.serializers import RaceSerializer


RACES_URL = reverse("api:race-list")

print(RACES_URL)


class CrudRaceTests(TestCase):
    """Test Crud operation on Race api"""

    def setUp(self):
        self.client = APIClient()

    def test_retrive_races(self):
        """Test retriving all races"""
        Race.objects.create(name="Wielka Prehyba", start_date="2019-04-27")
        Race.objects.create(name="Bieg 7 Dolin", start_date="2018-09-27")
        res = self.client.get(RACES_URL)
        races = Race.objects.all()
        serializer = RaceSerializer(races, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
