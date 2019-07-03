import pytest
from app.app import flask_app


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    client = flask_app.test_client()
    yield client
