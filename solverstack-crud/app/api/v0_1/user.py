from flask import make_response, request

from app import db
from app.models import User

from . import bp, errors


@bp.route("/user", methods=["GET", "POST"])
def user():
    if request.method == "GET":
        user = User.query.get_or_404(1).to_dict()

        return make_response({"user": user}, 200)

    if request.method == "POST":
        if not request.is_json:
            raise errors.InvalidUsage(
                "Incorrect request format! Request data must be JSON"
            )

        data = request.get_json(silent=True)
        if not data:
            raise errors.InvalidUsage(
                "Invalid JSON received! Request data must be JSON"
            )

        if "user" in data:
            user = data["user"]
        else:
            raise errors.InvalidUsage("'user' missing in request data")

        if not isinstance(user, dict):
            raise errors.InvalidUsage("'user' should be a dict")

        if not user:
            raise errors.InvalidUsage("'user' is empty")

        # Using dict unpacking for creation
        new_user = User(**{key: user[key] for key in user if key != "password"})
        new_user.set_password(user["password"])
        db.session.add(new_user)

        db.session.commit()

        user["id"] = new_user.id

        return make_response({"user": new_user.to_dict()}, 201)


@bp.route("/user/<string:username>", methods=["GET", "PUT"])
def user_one(username: str):
    if request.method == "GET":
        user = User.query.filter_by(username=username).first()

        if not user:
            raise errors.InvalidUsage("username not found")

        return make_response({"user": user.to_dict()}, 200)

    if request.method == "PUT":
        user = User.query.filter_by(username=username).first()

        if not request.is_json:
            raise errors.InvalidUsage(
                "Incorrect request format! Request data must be JSON"
            )

        data = request.get_json(silent=True)
        if not data:
            raise errors.InvalidUsage(
                "Invalid JSON received! Request data must be JSON"
            )

        params = ["username", "password"]

        new_user = {}

        for param in params:
            if param in data:
                new_user[param] = data[param]
            else:
                raise errors.InvalidUsage(f"{param} missing in request data")

        # Update values in DB
        user.username = new_user["latitude"]
        user.set_password(new_user["password"])

        db.session.commit()

        return make_response(new_user.to_dict(), 201)
