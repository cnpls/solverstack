import json
import logging

from . import common

ENDPOINT = f"{common.BASE_URL}/stack"
STACK = {"stack": {"name": ""}, "chain": [{"id": ""}, {"id": ""}]}


def test_stack_endpoint(client, auth_header: dict):
    logging.debug(f"input_data: {common.TEST_USER}")
    logging.debug(f"endpoint: {ENDPOINT}")

    response = client.post(ENDPOINT, headers=auth_header, json=STACK)
    output = json.loads(response.data)

    assert output
