from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient
from api.models import Race
from api.serializers import RaceSerializer, RaceResultSerializer
from .factories import RaceFactory, RaceResultFactory

RACES_URL = reverse("api:race-list")


class CrudRaceTests(TestCase):
    """Test Crud operation on Race api"""

    def setUp(self):
        self.client = APIClient()

    def test_retrive_races(self):
        """Test retriving all races"""
        RaceFactory.create(name="Wielka Prehyba", start_date="2019-04-27")
        RaceFactory.create(name="Bieg 7 Dolin", start_date="2018-09-27")
        res = self.client.get(RACES_URL)
        races = Race.objects.all()
        serializer = RaceSerializer(races, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_race(self):
        """Test creating race"""
        payload = dict(
            name="Wielka Prehyba",
            start_date="2019-04-27",
            distance=43.3,
            elevation_gain=1925,
            elevation_lost=1925,
            itra=2,
            food_point=3,
            time_limit=9,
        )
        res = self.client.post(RACES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        race = Race.objects.get(id=res.data["id"])
        self.assertEqual(payload["name"], getattr(race, "name"))
        self.assertEqual(
            payload["start_date"], str(getattr(race, "start_date"))
        )
        self.assertEqual(payload["distance"], float(getattr(race, "distance")))
        self.assertEqual(
            payload["elevation_gain"], getattr(race, "elevation_gain")
        )
        self.assertEqual(payload["itra"], getattr(race, "itra"))


class CrudRaceResultTests(TestCase):
    """Test Crud operation on Race Result api"""

    def test_create_race_result(self):
        """Test creation of race result"""
        race = RaceFactory.create()
        r_url = reverse("api:race-results-list", args=[race.id])
        payload = {
            "runner_name": "Michal Mojek",
            "runner_birth": "1980",
            "time_result": "03:30:29",
        }
        res = self.client.post(r_url, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_race_result_with_wrong_race(self):
        """Test failed creation race result with wrong race id"""
        r_url = reverse("api:race-results-list", args=[100])
        payload = {
            "runner_name": "Michal Mojek",
            "runner_birth": "1980",
            "time_result": "03:30:29",
        }
        res = self.client.post(r_url, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrive_race_results_list(self):
        race = RaceFactory.create()
        RaceResultFactory.create(race=race, runner_name="Test name")
        RaceResultFactory.create(race=race)
        r_url = reverse("api:race-results-list", args=[race.id])
        res = self.client.get(r_url)
        race_results = race.race_results.all()
        serializer = RaceResultSerializer(race_results, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
