import json
import logging

from . import common

ENDPOINT = f"{common.BASE_URL}/route"
ROUTES = [
    {
        "demand_id": "",
        "depot_id": "",
        "vehicle_id": "",
        "stop_number": "",
        "unit": "",
    }
] * 4


def test_route_endpoint(client, auth_header):
    input_data = {"routes": ROUTES, "stack_id": 1}
    logging.debug(f"input_data: {input_data}")
    logging.debug(f"endpoint: {ENDPOINT}")

    response = client.post(ENDPOINT, headers=auth_header, json=input_data)
    output = json.loads(response.data)

    assert output
