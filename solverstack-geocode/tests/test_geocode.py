import json
import logging
from typing import List

from pandas import DataFrame

from app import geocode

from . import common


def test_main_procedure(client, auth_header: dict, data: List[dict]):
    input_data = {"stack_id": 1, "zipcodes": data}
    logging.debug(f"input data : {input_data}")
    logging.debug(f"endpoint: {common.ENDPOINT}")

    response = client.post(common.ENDPOINT, headers=auth_header, json=input_data)
    output = json.loads(response.get_data())

    assert len(output["geocodes"]) == len(data)


def test_geocode(df: DataFrame):
    zipcodes = df.zipcode.str.zfill(5).tolist()
    countries = df.country.str.lower()

    len(zipcodes) == len(geocode.geocode_zipcodes(zipcodes, countries))
