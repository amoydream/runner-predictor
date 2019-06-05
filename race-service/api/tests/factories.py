from api import models
import factory


class RaceGroupFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.RaceGroup

    name = "Wielka Prehyba"


class RaceFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Race

    name = "Wielka Prehyba 2018"
    start_date = "2019-04-27"
    distance = 43.3
    elevation_gain = 1925
    elevation_lost = 1925
    itra = 2
    food_point = 3
    time_limit = 9


class RaceResultFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.RaceResult

    runner_name = "Michał Mojek"
    runner_birth = 1980
    time_result = "6:20:45"
