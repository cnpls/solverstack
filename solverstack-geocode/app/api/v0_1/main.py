import logging
from json import loads

import requests
from flask import jsonify, make_response, request

from app import geocode

from . import bp

CRUD_URL = "http://127.0.0.1:5002/api/v0.1/geocode"


@bp.route("/geocode", methods=["POST"])
def geocode_procedure():
    """
    Main RPC endpoint for passing input data for geocoded outputs.

    :zipcode:      str of 5-digit padded zipcodes
    :country:      str of country abbreviations
    """
    body: dict = loads(request.data)
    stack_id: int = body["stack_id"]

    zipcodes: list = [None] * len(body["zipcodes"])
    countries: list = [None] * len(body["zipcodes"])

    for i, row in enumerate(body["zipcodes"]):
        zipcodes[i]: str = row["zipcode"].strip()[:5].zfill(5)
        countries[i]: str = row["country"].strip()

    geocodes: list = geocode.geocode_zipcodes(zipcodes, countries)

    results = {"stack_id": stack_id, "geocodes": []}

    for i, geo in enumerate(geocodes):
        new_data = body["zipcodes"][i]
        new_data["latitude"] = geo[0]
        new_data["longitude"] = geo[1]

        results["geocodes"].append(new_data)

    try:
        if not request.headers.get("Authorization"):
            raise ValueError("Unauthorized request")

        response = requests.post(
            CRUD_URL,
            headers=request.headers,
            json=results,
        )

        return make_response(jsonify(loads(response.text)), 200)

    except Exception as e:
        logging.error(e)

        return make_response(jsonify(results), 200)
