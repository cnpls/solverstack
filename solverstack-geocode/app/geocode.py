import numpy as np
import pgeocode


def geocode_zipcodes(zipcodes: list, countries: list):
    """
    Use pgeocode to get latitude and longitude for zipcodes.

    :zipcodes:      list-like of clean zipcodes
    :countries:     list-like of expected country abbreviations

    :return:        list of lists containing [[lat, lon], ...]
    """
    geocodes = []

    for i, country in enumerate(countries):
        nomi = pgeocode.Nominatim(country)
        results = nomi.query_postal_code(zipcodes[i])

        lat = np.nan_to_num(results.latitude)
        lon = np.nan_to_num(results.longitude)

        geocodes.append([lat, lon])

    return geocodes
