export const checkFileData = (data: Object) => {
    /** 
     * Form utility check for geocodes.
     * 
     * TODO: add unit data check.
     */
    if (!data[0].hasOwnProperty("latitude") || !data[0].hasOwnProperty("longitude")) {
        alert("latitude and longitude fields are required in the damand file!");
    }
}

export const checkNum = (val: any) => {
    /**
     * Form utility check for numeric values.
     */
    if (!isFinite(val)) {
        alert("value is not a number!");
    }
}

export const checkUnit = (unit: String, data: any) => {
    /**
     * Form utitlity check for validating that the 
     * *unit* field exists in the data provided.
     */
    if (!data[0].hasOwnProperty(unit)) {
        alert("unit entered cannot be found in the demand file!");
    }
}

export const createRoutes = (oLat: number, oLon: number, demand: any, vehicles: Array<number>, stopNums: Array<number>) => {
    /**
     * Create list of objects {stops: [[oLon, oLat] ...]} where
     * origin is the first and last stop.
     * 
     * TODO: use stops for order.
     */
    let routed = {};

    for (var i = 0; i < demand.length; i++) {
        const coordinates = [parseFloat(demand[i].longitude), parseFloat(demand[i].latitude)];

        if (routed.hasOwnProperty(vehicles[i])) {
            routed[vehicles[i]].stops.push(coordinates);
        } else {
            routed[vehicles[i]] = {
                stops: [[oLon, oLat], coordinates]
            }
        }
    }

    // convert routes to list of objects
    const keys = Object.keys(routed);
    let routes = Array(keys.length);

    for (var i = 0; i < keys.length; i++) {
        let route = routed[keys[i]];
        const allStops = route.stops.concat([[oLon, oLat]]);
        routes[i] = {stops: allStops};
    }

    return routes;
}