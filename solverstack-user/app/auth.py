from datetime import timedelta
from json import loads

import requests
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash

CRUD_URL = "http://27.0.0.1:5002/api/v0.1/user"


def create_token(user: dict):
    identity = {key: user[key] for key in user if "password" not in key}
    token = create_access_token(identity=identity, expires_delta=timedelta(hours=5))

    return token


def authenticate(username, password):
    response = requests.get(f"{CRUD_URL}/{username}")

    if response.status_code != 200:
        return None

    user = loads(response.text)["user"]
    if check_password_hash(user["password_hash"], password):
        return create_token(user)

    return None
