from django.urls import reverse
from rest_framework import status
from api.models import Runner
from .factories import RunnerFactory
import pytest

RUNNERS_URL = reverse("api:runner-list")


@pytest.mark.django_db
class TestRunnerApi:
    def test_runner_creation_with_short_birth(self, client):
        payload = dict(name="Michał Mojek", birth_year=80)
        res = client.post(RUNNERS_URL, payload)
        assert res.status_code == status.HTTP_201_CREATED
        runner = Runner.objects.get(id=res.data["id"])
        assert runner.birth_year == 1980

    def test_runner_creation(self, client):
        payload = dict(name="Michał Mojek", birth_year=1980)
        res = client.post(RUNNERS_URL, payload)
        assert res.status_code == status.HTTP_201_CREATED

    def test_runner_creation_with_to_lower_date(self, client):
        payload = dict(name="Michał Mojek", birth_year=1800)
        res = client.post(RUNNERS_URL, payload)
        assert res.status_code == status.HTTP_400_BAD_REQUEST

    def test_runner_creation_with_blank_birth(self, client):
        payload = dict(name="Michał Mojek", birth_year="")
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
        payload = dict(name="Michał Mojek", birth_year=1980)
        res = client.post(endpoint, payload)
        assert res.status_code == status.HTTP_201_CREATED
        res2 = client.post(endpoint, payload)
        assert res2.status_code == status.HTTP_200_OK
