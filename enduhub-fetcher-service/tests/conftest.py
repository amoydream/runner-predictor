import pytest
from app.app import flask_app


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    client = flask_app.test_client()
    yield client


@pytest.fixture
def dict_results():
    return dict(
        runner_name="Michał Mojek",
        race_name="Prehyba2",
        distance="64 km",
        race_date="2018-12-14",
        runner_birth="1990",
        result_of_the_race="03:57:33",
        race_type="bieganie",
    )


@pytest.fixture
def html_with_results():
    return open("tests/enduhub_pawel_wojcik.html").read()
