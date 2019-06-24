from django.urls import reverse
from rest_framework import status
from api.models import Runner
from .factories import RunnerFactory
import pytest

RUNNERS_URL = reverse("api:runner-list")


@pytest.mark.django_db
class TestRunnerApi:
    def test_runner_creation_with_short_birth(self, client):
        payload = dict(name="Michał Mojek", birth_year=80, sex="M")
        res = client.post(RUNNERS_URL, payload)
        assert res.status_code == status.HTTP_201_CREATED
        runner = Runner.objects.get(id=res.data["id"])
        assert runner.birth_year == 1980

    def test_runner_creation(self, client):
        payload = dict(name="Michał Mojek", birth_year=1980, sex="M")
        res = client.post(RUNNERS_URL, payload)
        assert res.status_code == status.HTTP_201_CREATED

    def test_runner_creation_birth_strange(self, client):
        payload = dict(name="Michal Mojek", birth_year="—", sex="M")
        res = client.post(RUNNERS_URL, payload)
        assert res.status_code == status.HTTP_400_BAD_REQUEST

    def test_runner_creation_with_to_lower_date(self, client):
        payload = dict(name="Michał Mojek", birth_year=1800, sex="M")
        res = client.post(RUNNERS_URL, payload)
        assert res.status_code == status.HTTP_400_BAD_REQUEST

    def test_runner_creation_with_blank_birth(self, client):
        payload = dict(name="Michał Mojek", birth_year="", sex="M")
        res = client.post(RUNNERS_URL, payload)
        assert res.status_code == status.HTTP_400_BAD_REQUEST

    def test_runner_list(self, client):
        RunnerFactory.create(name="name1")
        RunnerFactory.create(name="name2")
        res = client.get(RUNNERS_URL)
        assert res.status_code == status.HTTP_200_OK
        assert len(res.data) == 2

    def test_get_or_create_point(self, client):
        endpoint = reverse("api:runner-get-or-create")
        payload = dict(name="Michał Mojek", birth_year=1980, sex="M")
        res = client.post(endpoint, payload)
        assert res.status_code == status.HTTP_201_CREATED
        res2 = client.post(endpoint, payload)
        assert res2.status_code == status.HTTP_200_OK

    def test_get_or_create_point_birth_error(self, client):
        endpoint = reverse("api:runner-get-or-create")
        payload = dict(name="Michał Mojek", birth_year="—", sex="M")
        res = client.post(endpoint, payload)
        assert res.status_code == status.HTTP_400_BAD_REQUEST

    def test_race_result_creation(self, client):
        """Test creation of race result"""
        runner = RunnerFactory.create()
        r_url = reverse("api:race-results-list", args=[runner.id])
        payload = {
            "event_name": "Wielka prehyba",
            "distance": "43.5",
            "race_date": "2019-04-27",
            "result_of_the_race": "06:30:29",
            "race_type": "bieg górski",
        }

        res = client.post(r_url, payload)
        print(res.content)
        assert res.status_code == status.HTTP_201_CREATED

    def test_race_result_creation_with_km(self, client):
        """Test creation of race result -  distance with km"""
        runner = RunnerFactory.create()
        r_url = reverse("api:race-results-list", args=[runner.id])
        payload = {
            "event_name": "Wielka prehyba",
            "distance": "64.5 km",
            "race_date": "2019-04-27",
            "result_of_the_race": "06:30:29",
            "race_type": "bieg górski",
        }

        res = client.post(r_url, payload)
        print(res.content)
        assert res.status_code == status.HTTP_201_CREATED
        assert res.data["distance"] == "64.5"

    def test_race_result_creation_with_maraton(self, client):
        """Test creation of race result -  distance with maraton string"""
        runner = RunnerFactory.create()
        r_url = reverse("api:race-results-list", args=[runner.id])
        payload = {
            "event_name": "Wielka prehyba",
            "distance": "maraton",
            "race_date": "2019-04-27",
            "result_of_the_race": "06:30:29",
            "race_type": "bieg górski",
        }

        res = client.post(r_url, payload)
        print(res.content)
        assert res.status_code == status.HTTP_201_CREATED
        assert res.data["distance"] == "42.1"

    def test_find_runner(self, client):
        RunnerFactory.create(name="Michał Mojek", birth_year=1980, sex="M")
        RunnerFactory.create(name="Jan Kowalski", birth_year=1979, sex="M")
        RunnerFactory.create(name="Jan Kowalski", birth_year=1970, sex="M")
        payload = dict(name="Michał Mojek", birth_year=1980)
        res = client.get(RUNNERS_URL, payload)
        assert res.status_code == status.HTTP_200_OK
        assert len(res.data) == 1
        res = client.get(RUNNERS_URL)
        assert len(res.data) == 3
