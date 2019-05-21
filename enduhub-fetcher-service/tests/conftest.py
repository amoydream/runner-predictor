import pytest
from app.app import flask_app


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    client = flask_app.test_client()
    yield client


@pytest.fixture
def html_with_results():
    return open("tests/enduhub_pawel_wojcik.html").read()
