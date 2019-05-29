from pytest_factoryboy import register

from .factories import RunnerFactory, RaceResultFactory

register(RunnerFactory)
register(RaceResultFactory)
