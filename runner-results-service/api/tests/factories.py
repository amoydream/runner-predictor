import factory
from api import models


class RunnerFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Runner

    name = "Michał Mojek"
    birth_year = 1980
