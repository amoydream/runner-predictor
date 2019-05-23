import pytest
from api.models import Runner, RaceResult


@pytest.mark.django_db
class TestModels:
    def test_runner_str_representation(self):
        runner = Runner.objects.create(name="Michał Mojek", birth_year=1980)
        runner.save()
        runner = Runner.objects.get(id=runner.id)
        assert str(runner) == "Michał Mojek, 1980"

    def test_runner_birth_year_with_short_format(self):
        runner = Runner.objects.create(name="Michał Mojek", birth_year=80)
        runner.save()
        runner = Runner.objects.get(id=runner.id)
        assert runner.birth_year == 1980

    # def test_runner_birth_valid(self):
    #     runner = Runner.objects.create(name="Michał Mojek", birth_year=1900)
    #     with pytest.raises(ValidationError):
    #         runner.full_clean()

    def test_race_result_creation(self, runner):
        race_result = RaceResult.objects.create(
            runner=runner,
            event_name="Event",
            distance=10.163,
            race_date="2019-03-31",
            result_of_the_race="6:23:29",
            race_type="Biegi Górskie",
        )
        race_result.refresh_from_db()
        assert race_result.runner == runner
