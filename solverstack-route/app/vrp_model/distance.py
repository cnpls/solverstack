from typing import List

import numpy as np
from haversine import Unit, haversine_vector


def create_vectorized_haversine_li(
    olat: float,
    olon: float,
    dlats: List[float],
    dlons: List[float],
    dist_factor: float = 1.17,
) -> List[float]:
    assert len(dlats) == len(dlons)

    olats = [olat] * len(dlats)
    olons = [olon] * len(dlons)
    os = list(zip(olats, olons))
    ds = list(zip(dlats, dlons))

    ds = haversine_vector(os, ds, unit=Unit.MILES)

    # distance factor adjust haversine for theoretical travel difference
    ds *= dist_factor

    return ds


def create_matrix(
    origin_lat: float,
    origin_lon: float,
    dest_lats: List[float],
    dest_lons: List[float],
    int_precision: int = 100,
) -> List[List[int]]:
    """
    creates matrix using optimized matrix processing. distances
    are converted to integers (x*100).

    :_origin:    (origin.lat: float, origin.lon: float)
    :_dests:     list of demands; (demand.lat, demand.lon)

    returns _matrix: list[list, ..., len(origin+dests)]
    """
    lats = [origin_lat] + dest_lats
    lons = [origin_lon] + dest_lons

    assert len(lats) == len(lons)

    matrix = []
    for i in range(len(lats)):
        fdistances = create_vectorized_haversine_li(
            olat=lats[i], olon=lons[i], dlats=lats, dlons=lons
        )

        idistances = np.ceil(fdistances * int_precision).astype(int)
        matrix.append(idistances)

    return matrix
