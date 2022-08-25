# flake8: noqa
from flask_jwt_extended import create_access_token

from app import __version__, create_app
from config import Config

BASE_URL: str = f"/api/{__version__}"
TEST_USER: dict = {"id": 1, "username": "test", "password": "password"}
