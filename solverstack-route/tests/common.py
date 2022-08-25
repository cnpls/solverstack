import logging
import os

import pandas as pd

TEST_ROOT = os.path.dirname(os.path.abspath(__file__))
CSV_TESTING_FILENAME = "vrp_testing_data.csv"
CSV_TESTING_FILEPATH = os.path.join(TEST_ROOT, CSV_TESTING_FILENAME)


def get_csv():
    logging.debug(f"filepath: {CSV_TESTING_FILEPATH}.")

    df = pd.read_csv(CSV_TESTING_FILEPATH)
    df.pallets = df.pallets.fillna(1)

    return df


TESTING_CSV_DF = get_csv()


def get_vrp_unit_name_basic():
    name = "pallets"
    logging.debug(f"unit name: {name}.")

    return name


def get_vrp_units_basic():
    """demand units must have 0 for origin node"""
    units = ["0", "5", "10", "2", "4", "12", "6", "14"]
    logging.debug(f"demand units: {units}")

    return units


def get_vrp_unit_name_csv():
    name = "pallets"
    logging.debug(f"unit name: {name}")

    return name


def get_vrp_units_csv():
    """demand units must have 0 for origin node"""
    units = [0] + TESTING_CSV_DF.pallets.fillna(1).astype(str).tolist()
    logging.debug(f"demand units: {units}")

    return units


def get_vrp_data():
    # TODO: abstract json def
    lat, lon = 41.4191, -87.7748
    logging.debug(f"origin lat: {lat}, lon: {lon}.")

    origin = {"location": {"latitude": lat, "longitude": lon}}

    origin_lat = origin["location"]["latitude"]
    origin_lon = origin["location"]["longitude"]

    return {
        "origin": {
            "location": {"latitude": origin_lat, "longitude": origin_lon}
        },
        "unit": "pallets",
        "demands": TESTING_CSV_DF.to_dict("records"),
        "vehicle_max_capacity_quantity": "26",
        "vehicle_definitions": None,  # TODO
    }


vrp_data = get_vrp_data()
