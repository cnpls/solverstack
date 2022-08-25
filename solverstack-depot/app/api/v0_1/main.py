import logging
from json import loads

import requests
from flask import jsonify, make_response, request
from numpy import zeros

from app import depot

from . import bp


# CRUD_URL = "http://solverstack_crud:5002/api/v0.1/depot"
CRUD_URL = "http://127.0.0.1:5002/api/v0.1/depot"


@bp.route("/depot", methods=["POST"])
def depot_procedure():
    """
    Main RPC endpoint for passing input data for origin output.

    :latitude:      str of destination latitudes
    :longitude:     str of destination longitudes
    """
    body = loads(request.data)
    stack_id = body["stack_id"]
    nodes = body["nodes"]

    lats = zeros(len(nodes))
    lons = zeros(len(nodes))

    for i, row in enumerate(nodes):
        lats[i] = row["latitude"]
        lons[i] = row["longitude"]

    results = depot.create_origin(lats, lons)

    try:

        if not request.headers.get("Authorization"):
            raise ValueError("Unauthorized request")

        response = requests.post(
            CRUD_URL,
            headers=request.headers,
            json={"stack_id": stack_id, "depots": [results]},
        )

        return make_response(jsonify(loads(response.text)), 200)

    except Exception as e:
        logging.error(e)

        return make_response(
            jsonify({"stack_id": stack_id, "depots": [results]}), 200
        )
