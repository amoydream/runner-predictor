from api import models
import factory


class RaceFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Race

    name = "Wielka Prehyba"
    start_date = "2019-04-27"
    distance = 43.3
    elevation_gain = 1925
    elevation_lost = 1925
    itra = 2
    food_point = 3
    time_limit = 9
