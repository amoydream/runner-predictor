import pytest
from django.core.exceptions import ValidationError


@pytest.mark.django_db
class TestModels:
    @pytest.mark.parametrize("runner__birth_year", [1980])
    @pytest.mark.parametrize("runner__name", ["Michał Mojek"])
    @pytest.mark.parametrize("runner__sex", ["M"])
    def test_runner_str_representation(self, runner):
        assert str(runner) == "Michał Mojek, 1980, M"

    @pytest.mark.parametrize("runner__name", ["Michał Mojek"])
    def test_runner_str_representation_dash(self, runner):
        with pytest.raises(ValidationError):
            runner.birth_year = "—"
            runner.save()

    @pytest.mark.parametrize("runner__birth_year", [80])
    def test_runner_birth_year_with_short_format(self, runner):
        runner.refresh_from_db()
        assert runner.birth_year == 1980

    def test_race_result_creation(self, runner, race_result):
        race_result.refresh_from_db()
        assert race_result.runner == runner

    @pytest.mark.parametrize("race_result__distance", ["64.5 km"])
    def test_race_result_distance_with_km(self, race_result):
        race_result.refresh_from_db()
        assert race_result.distance == 64.5

    @pytest.mark.parametrize("race_result__distance", ["maraton"])
    def test_race_result_distance_with_maraton(self, race_result):
        race_result.refresh_from_db()
        assert float(race_result.distance) == 42.1

    @pytest.mark.parametrize("race_result__distance", ["Maraton"])
    def test_race_result_distance_with_maraton(self, race_result):
        race_result.refresh_from_db()
        assert float(race_result.distance) == 42.1

    def test_race_result_distance_with_unknown(self, race_result):
        with pytest.raises(ValidationError):
            race_result.distance = "uknown_distance"
            race_result.save()
