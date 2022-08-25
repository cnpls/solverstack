import logging
import os

import pandas as pd
import pytest
from flask_jwt_extended import create_access_token

from app import create_app
from config import Config

TEST_ROOT = os.path.dirname(os.path.abspath(__file__))
TEST_USER = {"id": 1, "username": "test", "password": "password"}
CSV_TESTING_FILENAME = "zipcode_testing_data.csv"
CSV_TESTING_FILEPATH = os.path.join(TEST_ROOT, CSV_TESTING_FILENAME)


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"


@pytest.fixture()
def client():
    yield create_app(TestConfig).test_client()


@pytest.fixture()
def auth_header():
    app = create_app(TestConfig)

    with app.app_context():
        token = create_access_token(TEST_USER)

    headers: dict = {"Authorization": "Bearer {}".format(token)}

    return headers


@pytest.fixture()
def df():
    types = {"zipcode": str, "country": str}
    df = pd.read_csv(CSV_TESTING_FILEPATH, dtype=types)
    logging.debug(f"filepath: {CSV_TESTING_FILEPATH} size: {df.shape}")

    return df


@pytest.fixture()
def data(df):
    data = [
        {
            "zipcode": df.zipcode.iloc[i],
            "country": df.country.iloc[i],
        }
        for i in range(len(df))
    ]

    return data
