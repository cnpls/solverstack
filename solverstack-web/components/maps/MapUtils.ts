import * as mapTypes from "./MapTypes";


// TODO refactor exported functions
export const markerIsContiguousUsa = (lat: Number, lon: Number) => {
    if (lat >= 19.50139 && lat <= 64.85694 && lon >= -161.75583 && lon <= -68.01197) {
        return true;
    }
    
    return false;
}

export const markersAreContiguousUsa = (markers: any) => {
    for (let i = 0; i < markers.length; i++) {
        if (!markerIsContiguousUsa(markers[i].latitude, markers[i].longitude)) {
            return false;
        }
    }

    return true;
}

export const isNullIsland = (lat: number, lon: number) => {
    if (lat == 0. && lon == 0.) {
        return true;
    }

    return false;
}

export const getAverageGeocodes = (markers: Array<mapTypes.CoordinateMarker>) => {
    /**
     * Calculates average of coordinates and returns
     * as list [lat, lon]
     */
    let latSum = 0, lonSum = 0;

    if (markers.length == 0) {
        return [0., 0.];
    }

    for (var i = 0; i < markers.length; i++) {
        latSum = latSum + markers[i].latitude;
        lonSum = lonSum + markers[i].longitude;
    }
    
    let center = [latSum / markers.length, lonSum / markers.length];

    return center;
}