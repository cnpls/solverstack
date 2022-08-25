import json
import logging

from app import depot

from . import common


def test_main_procedure(client, auth_header, data):
    input_data = {"stack_id": 1, "nodes": data}
    logging.debug(f"input data : {input_data}")

    logging.debug(f"endpoint: {common.ENDPOINT}")

    headers = dict(auth_header, **{"Content-Type": "application/json"})
    response = client.post(common.ENDPOINT, headers=headers, json=input_data)
    output = json.loads(response.get_data())

    assert len(output) == 2
    assert all(ele in output["depots"][0] for ele in ["latitude", "longitude"])


def test_create_depot(df):
    lats = df.latitude.tolist()
    lons = df.longitude.tolist()

    assert depot.create_origin(lats, lons)
