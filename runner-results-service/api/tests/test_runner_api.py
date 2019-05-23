from django.urls import reverse
from rest_framework import status
from api.models import Runner
import pytest

RUNNERS_URL = reverse("api:runner-list")


@pytest.mark.django_db
class TestRunnerApi:
    def test_runner_creation_with_short_birth(self, client):
        payload = dict(name="Michał Mojek", birth_year=80)
        res = client.post(RUNNERS_URL, payload)
        print(res.content)
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
        print(res.content)
        assert res.status_code == status.HTTP_400_BAD_REQUEST
