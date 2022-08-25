from random import randint

from app.vrp_model import distance

from . import common


class TestVRPData:
    def test_vrp_origin_data(self, origin):
        origin_lat = origin["latitude"]
        origin_lon = origin["longitude"]

        assert isinstance(origin_lat, float)
        assert -90 < origin_lat < 90

        assert isinstance(origin_lon, float)
        assert -180 < origin_lon < 180

    def test_vrp_demand_data(self):
        demand_unit_name = common.get_vrp_unit_name_basic()

        assert isinstance(demand_unit_name, str)
        assert len(demand_unit_name) > 0


def test_matrix():
    olat, olon = 41.4191, -87.7748
    dlats = common.TESTING_CSV_DF.latitude.tolist()
    dlons = common.TESTING_CSV_DF.longitude.tolist()
    matrix = distance.create_matrix(
        origin_lat=olat, origin_lon=olon, dest_lats=dlats, dest_lons=dlons
    )

    assert len(dlats) == len(dlons)

    i = randint(0, len(matrix) - 1)

    assert len(matrix) == len(matrix[i]) == len(dlats) + 1
