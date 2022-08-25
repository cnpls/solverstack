from json import loads

import requests
from flask import jsonify, make_response, request

from app import auth

from . import bp


CRUD_URL = "http://127.0.0.1:5002/api/v0.1/user"


@bp.route("/login", methods=["POST"])
def login():
    """
    TODO
    """
    body = loads(request.data)

    token = auth.authenticate(body["username"], body["password"])

    if not token:
        return make_response("failed to authenticate", 400)

    response = {"token": token, "username": body["username"]}

    return make_response(jsonify(response), 200)


@bp.route("/register", methods=["POST"])
def register():
    """
    TODO
    """
    body = loads(request.data)

    response = requests.get(f"{CRUD_URL}/{body['username']}")
    if response.status_code == 200:
        return make_response("username exists", 400)

    user = loads(requests.post(CRUD_URL, json={"user": body}).text)["user"]
    token = auth.create_token(user)

    response = {"token": token, "username": user["username"]}

    return make_response(jsonify(response), 200)
