import factory
from api import models


class RunnerFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Runner

    name = "Michał Mojek"
    birth_year = 1980


class RaceResultFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.RaceResult

    runner = factory.SubFactory(RunnerFactory)
    event_name = "Event"
    distance = 10.163
    race_date = "2019-03-31"
    result_of_the_race = "6:23:29"
    race_type = "Biegi Górskie"
