import pytest

from app import create_app
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"


@pytest.fixture
def client():
    yield create_app(TestConfig).test_client()


def test_register(client):
    # TODO: figure out isolated testing for cross-service features
    return

    # input_data = {"username": "test1", "password": "password"}
    # logging.debug(f"input data : {input_data}")

    # endpoint = f"/api/{__version__}/register"
    # logging.debug(f"endpoint: {endpoint}")

    # token = client.post(endpoint, json=input_data).data

    # assert token


def test_login(client):
    # TODO: figure out isolated testing for cross-service features
    return

    # input_data = {"username": "test1", "password": "password"}
    # logging.debug(f"input data : {input_data}")

    # endpoint = f"/api/{__version__}/login"
    # logging.debug(f"endpoint: {endpoint}")

    # token = client.post(endpoint, json=input_data).data

    # assert token
