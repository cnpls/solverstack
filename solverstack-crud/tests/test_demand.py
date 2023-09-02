import logging
import random
import string
from csv import DictReader
from typing import List

import pytest

from . import common

ENDPOINT = common.BASE_URL + "/demand"


@pytest.fixture()
def sample_demand():
    """Return rows of sample demand from csv file"""

    # Loading data from sample csv
    with open("tests/vrp_testing_data.csv") as sample_demand_file:
        sample_demand_rows = list(DictReader(sample_demand_file))

    NUM_CLUSTERS: int = 10

    # Cleaning individual objects in-place
    for demand in sample_demand_rows:
        demand.pop("zipcode")
        demand["latitude"] = float(demand["latitude"])
        demand["longitude"] = float(demand["longitude"])
        demand["quantity"] = float(demand.pop("weight")) / 10
        demand["unit"] = "kilograms"
        demand["cluster_id"] = int(demand.pop("pallets")) % NUM_CLUSTERS

    return sample_demand_rows


@pytest.fixture()
def random_demand():
    """Return random generated demand"""

    return {
        "latitude": random.uniform(-90, 90),
        "longitude": random.uniform(-180, 180),
        "quantity": random.uniform(0, 20000),
        "cluster_id": random.randint(0, 100),
        "unit": "".join(
            random.choices(string.ascii_lowercase, k=random.randint(1, 10))
        ),
    }


@pytest.mark.parametrize(
    "content_type",
    [
        "audio/aac",
        "application/x-abiword",
        "application/x-freearc",
        "video/x-msvideo",
        "application/vnd.amazon.ebook",
        "application/octet-stream",
        "image/bmp",
        "application/x-bzip",
        "application/x-bzip2",
        "application/x-csh",
        "text/css",
        "text/csv",
        "application/msword",
        ("application/vnd.openxmlformats-officedocument.wordprocessingml" ".document"),
        "application/vnd.ms-fontobject",
        "application/epub+zip",
        "application/gzip",
        "image/gif",
        "text/html",
        "image/vnd.microsoft.icon",
        "text/calendar",
        "application/java-archive",
        "image/jpeg",
        "text/javascript, per the following specifications:",
        "audio/midi",
        "text/javascript",
        "audio/mpeg",
        "video/mpeg",
        "application/vnd.apple.installer+xml",
        "application/vnd.oasis.opendocument.presentation",
        "application/vnd.oasis.opendocument.spreadsheet",
        "application/vnd.oasis.opendocument.text",
        "audio/ogg",
        "video/ogg",
        "application/ogg",
        "audio/opus",
        "font/otf",
        "image/png",
        "application/pdf",
        "application/x-httpd-php",
        "application/vnd.ms-powerpoint",
        (
            "application/vnd.openxmlformats-officedocument.presentationml"
            ".presentation"
        ),
        "application/vnd.rar",
        "application/rtf",
        "application/x-sh",
        "image/svg+xml",
        "application/x-shockwave-flash",
        "application/x-tar",
        "image/tiff",
        "video/mp2t",
        "font/ttf",
        "text/plain",
        "application/vnd.visio",
        "audio/wav",
        "audio/webm",
        "video/webm",
        "image/webp",
        "font/woff",
        "font/woff2",
        "application/xhtml+xml",
        "application/vnd.ms-excel",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "application/xml ",
        "application/vnd.mozilla.xul+xml",
        "application/zip",
        "video/3gpp",
        "video/3gpp2",
        "application/x-7z-compressed",
    ],
)
def test_non_json_request(client, content_type: str, auth_header: dict):
    """Test with content types other than 'application/json'"""

    logging.info(f"Testing with content-type : {content_type}")

    headers = dict(auth_header, **{"Content-Type": content_type})

    res = client.post(ENDPOINT, headers=headers, data="")

    logging.debug(f"Response : {res}")
    logging.debug(f"Response Data : {res.data}")

    assert res.status_code == 400
    assert res.headers["Content-Type"] == "application/json"
    assert res.json["message"] == "Incorrect request format! Request data must be JSON"


def test_invalid_json(client, auth_header: dict):
    """Test with invalid JSON in request"""

    logging.info("Testing with invalid JSON")
    logging.debug(f'Sending request to "{ENDPOINT}"')

    headers = dict(auth_header, **{"Content-Type": "application/json"})

    res = client.post(
        ENDPOINT,
        headers=headers,
        data="".join(
            random.choices(
                string.ascii_letters + "".join(["{", "}", '"', "'"]),
                k=random.randint(1, 27),
            )
        ),
    )

    logging.debug(f"Response : {res}")
    logging.debug(f"Response Data : {res.data}")

    assert res.status_code == 400
    assert res.headers["Content-Type"] == "application/json"
    assert res.json["message"] == "Invalid JSON received! Request data must be JSON"


def test_empty_demand(client, auth_header):
    """Test by sending empty demand array"""
    input_data = {"demand": []}
    logging.info("Testing with empty demand array")

    headers = dict(auth_header, **{"Content-Type": "application/json"})

    res = client.post(ENDPOINT, headers=headers, json=input_data)

    logging.debug(f"Response : {res}")
    logging.debug(f"Response Data : {res.data}")

    assert res.status_code == 400
    assert res.headers["Content-Type"] == "application/json"

    error_message = res.json["message"]
    assert error_message == "'demand' is empty"


@pytest.mark.parametrize(
    "param, value",
    [
        ("latitude", -101.536),
        ("latitude", "-101.536"),
        ("latitude", -846),
        ("latitude", "-846"),
        ("latitude", 507.305),
        ("latitude", "1.04"),
        ("latitude", 643),
        ("latitude", "75"),
        ("latitude", "abl{s"),
        ("latitude", ""),
        ("longitude", -967.895),
        ("longitude", "-967.895"),
        ("longitude", -816),
        ("longitude", "-816"),
        ("longitude", 2131.114),
        ("longitude", "2131.114"),
        ("longitude", 137),
        ("longitude", "137"),
        ("longitude", "itKv{a"),
        ("longitude", ""),
        ("cluster_id", -4830.546),
        ("cluster_id", -2113),
        ("cluster_id", 9326.594),
        ("cluster_id", "uHNHjdeb2"),
        ("cluster_id", ""),
        ("unit", -6813.875),
        ("unit", -3942),
        ("unit", 2959.333),
        ("unit", 1769),
        ("unit", "-23"),
        ("unit", "1832"),
        ("unit", "faf2"),
        ("unit", "knuw{"),
        ("unit", "}knuw"),
        ("unit", "!dead"),
        ("unit", ""),
        ("quantity", -1391.151),
        ("quantity", "-1391.151"),
        ("quantity", -4921),
        ("quantity", "-4921"),
        ("quantity", "   bsgj"),
        ("quantity", "hfuo6542w"),
        ("quantity", ""),
    ],
)
def test_invalid_demand(
    client, auth_header: dict, param: str, value: any, random_demand: dict
):
    """Test with invalid parameters in demand"""

    demand = random_demand
    input_data = {"demand": [demand], "stack_id": 1}
    logging.debug(f"Demand : {demand}")
    logging.debug(f"Input data : {input_data}")

    demand[param] = value
    logging.debug(f"Invalid demand : {demand}")

    headers = dict(auth_header, **{"Content-Type": "application/json"})

    res = client.post(ENDPOINT, headers=headers, json=input_data)

    assert res.status_code == 400
    assert f"Invalid {param}" in res.json["message"]


def test_single_insert(client, auth_header: dict, random_demand: dict):
    """Test with single demand"""
    demand = random_demand
    input_data = {"demand": [demand], "stack_id": 1}
    logging.debug(f"demand : {demand}")

    headers = dict(auth_header, **{"Content-Type": "application/json"})

    res = client.post(ENDPOINT, headers=headers, json=input_data)

    logging.debug(f"Response : {res}")
    logging.debug(f"Response data : {res.data}")

    assert res.status_code == 201
    assert res.headers["Content-Type"] == "application/json"

    for demand, response in zip([demand], res.json["demand"]):
        id = response.pop("id")
        assert isinstance(id, int)
        assert demand == response
        response["id"] = id


def test_batch_insert(client, auth_header: dict, sample_demand: List[dict]):
    """Test with multiple demand"""

    input_data = {"demand": sample_demand, "stack_id": 1}
    logging.info("Testing with multiple demand in one request")

    headers = dict(auth_header, **{"Content-Type": "application/json"})

    res = client.post(ENDPOINT, headers=headers, json=input_data)

    assert res.status_code == 201
    assert len(res.json["demand"]) == len(sample_demand)

    for demand, response in zip(sample_demand, res.json["demand"]):
        id = response.pop("id")
        assert isinstance(id, int)
        assert demand == response
        response["id"] = id
