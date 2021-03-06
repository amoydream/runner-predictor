from django.urls import reverse
from django.test import TestCase, RequestFactory

from rest_framework import status
from rest_framework.test import APIClient
from api.models import Race, RaceGroup
from api.serializers import (
    RaceSerializer,
    RaceResultSerializer,
    RaceGroupSerializer,
)
from .factories import RaceFactory, RaceResultFactory, RaceGroupFactory


from unittest.mock import patch

RACES_URL = reverse("api:race-list")
RACE_GROUP_URL = reverse("api:racegroup-list")


class CrudRaceGroupTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_retrive_group(self):
        """Test retriving all races group"""
        RaceGroupFactory.create(name="Wielka Prehyba")
        RaceGroupFactory.create(name="Rzeźniczek")
        res = self.client.get(RACE_GROUP_URL)
        races = RaceGroup.objects.all()
        serializer = RaceGroupSerializer(races, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


class CrudRaceTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_retrive_races(self):
        """Test retriving all races"""
        RaceFactory.create(name="Wielka Prehyba", start_date="2019-04-27")
        RaceFactory.create(name="Bieg 7 Dolin", start_date="2018-09-27")
        res = self.client.get(RACES_URL)
        races = Race.objects.all()

        serializer = RaceSerializer(
            races,
            many=True,
            context={"request": RequestFactory().get(RACES_URL)},
        )
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

    def test_race_results_url_endopoints_on_detail_race(self):
        race = RaceFactory.create()
        RaceResultFactory.create(race=race)
        RaceResultFactory.create(race=race, runner_name="Some runner")
        r_url = reverse("api:race-results-list", args=[race.id])
        res = self.client.get(reverse("api:race-detail", args=[race.id]))
        assert r_url in res.data["race_results_url"]


class CrudRaceResultTests(TestCase):
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

    def test_create_race_results_failed_with_dupilactions(self):

        race = RaceFactory.create()
        payload = {
            "runner_name": "Michal Mojek",
            "runner_birth": "1980",
            "time_result": "03:30:29",
        }
        r_url = reverse("api:race-results-list", args=[race.id])
        res = self.client.post(r_url, payload)
        res2 = self.client.post(r_url, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res2.status_code, status.HTTP_400_BAD_REQUEST)

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

    @patch("api.models.Race.download_from_enduhub")
    def test_donwload_enduhub(self, mock):
        race = RaceFactory.create()
        RaceResultFactory.create(race=race)
        endpoint = reverse("api:race-download-enduhub-data")
        payload = dict(race_id=race.id)
        res = self.client.post(endpoint, payload)
        assert res.status_code == status.HTTP_201_CREATED

    @patch("api.models.Race.download_from_itra")
    def test_donwload_itra(self, mock):
        race = RaceFactory.create()
        RaceResultFactory.create(race=race)
        endpoint = reverse("api:race-download-itra-data")
        print(endpoint)
        payload = dict(race_id=race.id)
        res = self.client.post(endpoint, payload)
        assert res.status_code == status.HTTP_201_CREATED
