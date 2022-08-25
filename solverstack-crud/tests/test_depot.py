import logging
import random
import string
from typing import List

import pytest

from . import common

ENDPOINT = common.BASE_URL + "/depot"


@pytest.fixture()
def random_depot():
    """Return random generated depot"""

    return {
        "latitude": random.uniform(-90, 90),
        "longitude": random.uniform(-180, 180),
    }


@pytest.fixture()
def random_depots(num_objects=20):
    """Return list of random depots"""
    return [
        {
            "latitude": random.uniform(-90, 90),
            "longitude": random.uniform(-180, 180),
        }
        for i in range(num_objects)
    ]


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
        (
            "application/vnd.openxmlformats-officedocument.wordprocessingml"
            ".document"
        ),
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
def test_non_json_request(client, auth_header: dict, content_type: str):
    """Test with content types other than 'application/json'"""

    logging.debug(f"Testing with content-type : {content_type}")

    headers = dict(auth_header, **{"Content-Type": content_type})

    res = client.post(ENDPOINT, headers=headers, data="")

    logging.debug(f"Response : {res}")
    logging.debug(f"Response Data : {res.data}")

    assert res.status_code == 400
    assert res.headers["Content-Type"] == "application/json"
    assert (
        res.json["message"]
        == "Incorrect request format! Request data must be JSON"
    )


def test_invalid_json(client, auth_header: dict):
    """Test with invalid JSON in request"""

    logging.debug("Testing with invalid JSON")
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
    assert (
        res.json["message"]
        == "Invalid JSON received! Request data must be JSON"
    )


def test_empty_depot(client, auth_header: dict):
    """Test by sending empty depot array"""

    logging.debug("Testing with empty 'depots' array")

    headers = dict(auth_header, **{"Content-Type": "application/json"})

    res = client.post(ENDPOINT, headers=headers, json={"depots": []})

    logging.debug(f"Response : {res}")
    logging.debug(f"Response Data : {res.data}")

    assert res.status_code == 400
    assert res.headers["Content-Type"] == "application/json"

    error_message = res.json["message"]
    assert error_message == "'depots' is empty"


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
    ],
)
def test_invalid_depot(
    client, auth_header: dict, param: str, value: any, random_depot: dict
):
    """Test with invalid parameters in depot"""

    depot = random_depot
    input_data = {"depots": [depot], "stack_id": 1}
    logging.debug(f"Depot : {depot}")
    logging.debug(f"Input data: {input_data}")

    depot[param] = value
    logging.debug(f"Invalid depot : {depot}")

    headers = dict(auth_header, **{"Content-Type": "application/json"})

    res = client.post(ENDPOINT, headers=headers, json=input_data)

    assert res.status_code == 400
    assert f"Invalid {param}" in res.json["message"]


def test_single_insert(client, auth_header: dict, random_depot: dict):
    """Test with single depot"""

    depot = random_depot
    input_data = {"depots": [depot], "stack_id": 1}
    logging.debug(f"Depot : {depot}")
    logging.debug(f"Input data: {input_data}")

    headers = dict(auth_header, **{"Content-Type": "application/json"})

    res = client.post(ENDPOINT, headers=headers, json=input_data)

    logging.debug(f"Response : {res}")
    logging.debug(f"Response Data : {res.data}")

    assert res.status_code == 201
    assert res.headers["Content-Type"] == "application/json"
    for depot, response in zip([depot], res.json["depots"]):
        id = response.pop("id")
        assert isinstance(id, int)
        assert depot == response
        response["id"]: int = id


def test_multiple_insert(client, auth_header: dict, random_depots: List[dict]):
    """Test with multiple objects in array"""

    input_data = {"stack_id": 1, "depots": random_depots}
    logging.debug(f"Number of depots : {len(random_depots)}")
    logging.debug(f"Input data: {input_data}")

    headers = dict(auth_header, **{"Content-Type": "application/json"})

    res = client.post(ENDPOINT, headers=headers, json=input_data)

    logging.debug(f"Response : {res}")
    logging.debug(f"Response Data : {res.data}")

    assert res.status_code == 400
    assert res.headers["Content-Type"] == "application/json"
    assert "contains more than one object" in res.json["message"]


def test_individual_get(client, auth_header: dict, random_depot: dict):
    """Test by inserting depot and GET from individual resource"""

    depot = random_depot
    depots = [depot]
    input_data = {"depots": depots, "stack_id": 1}
    logging.debug(f"Depot : {depot}")

    headers = dict(auth_header, **{"Content-Type": "application/json"})

    res = client.post(ENDPOINT, headers=headers, json=input_data)

    logging.debug(f"Response : {res}")
    logging.debug(f"Response Data : {res.data}")

    assert res.status_code == 201
    assert res.headers["Content-Type"] == "application/json"

    for depot, response in zip(depots, res.json["depots"]):
        id = response.pop("id")

        assert isinstance(id, int)
        assert depot == response

        response["id"] = id

        test_res = client.get(ENDPOINT + f"/{id}", headers=headers)

        logging.debug(f"Individual Response for id {id} : {test_res}")
        logging.debug(f"Individual Response Data : {test_res.data}")

        individual_depot = test_res.json
        individual_depot.pop("id")
        individual_depot.pop("stack_id")

        assert test_res.status_code == 200
        assert test_res.is_json
        assert individual_depot == depot


def test_individual_put(client, auth_header: dict, random_depot: dict):
    """Test by inserting depot and PUT from individual resource"""

    depots = [random_depot]
    input_data = {"depots": depots, "stack_id": 1}
    logging.debug(f"Depot: {random_depot}")
    logging.debug(f"Input data: {input_data}")

    headers = dict(auth_header, **{"Content-Type": "application/json"})

    res = client.post(ENDPOINT, headers=headers, json=input_data)

    logging.debug(f"Response : {res}")
    logging.debug(f"Response Data : {res.data}")

    assert res.status_code == 201
    assert res.is_json

    for depot, response in zip(depots, res.json["depots"]):
        id = response.pop("id")

        assert isinstance(id, int)

        # PUT individual endpoint data
        test_res = client.put(
            ENDPOINT + f"/{id}",
            headers=headers,
            json={"depot": random_depot, "stack_id": 1},
        )

        logging.debug(f"Individual Response for id {id} : {test_res}")
        logging.debug(f"Individual Response Data : {test_res.data}")

        assert test_res.status_code == 200
        assert test_res.is_json

        individual_depot = test_res.json["depot"]
        individual_depot.pop("id")
        individual_depot.pop("stack_id")

        assert individual_depot == depot
