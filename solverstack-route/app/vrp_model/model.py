"""TODO: omg refactor pls"""
from collections import namedtuple
from typing import List, Tuple

import numpy as np
from ortools.constraint_solver import pywrapcp, routing_enums_pb2

from app.vrp_model import cluster, distance


def get_dropped_nodes(model, assignment) -> List[int]:
    dropped = []
    for idx in range(model.Size()):
        if assignment.Value(model.NextVar(idx)) == idx:
            dropped.append(idx)

    return dropped


def get_solution_str(solution: List) -> str:
    _str = ""

    for i, r in enumerate(solution):
        _str += f"Route(idx={i})\n"
        s = "\n".join("{}: {}".format(*k) for k in enumerate(r))
        _str += s + "\n\n"

    return _str


def solve(
    nodes: List[Tuple[float, float]],
    distance_matrix: List[List[int]],
    time_matrix: List[List[int]],
    time_windows: List[Tuple[int, int]],
    demand: List[int],
    vehicle_caps: List[int],
    depot_index: int,
    constraints: Tuple[int, int, int],
    max_search_seconds: int = 5,
) -> List:
    """
    high level implementation of an ortools capacitated vehicle routing model.

    :nodes:                         list of tuples containing nodes (origin at
                                    index 0) with
                                    lat(float), lon(float)
    :distance_matrix:               [[int, int, int, ...], [...] ...] distance
                                    matrix of origin at node 0 and demand nodes
                                    at 1 -> len(matrix) - 1 processed at a
                                    known precision
    :demand_quantities:             [int, int, ... len(demand nodes) - 1]
    :vehicle_caps:                  list of integers for vehicle
                                    capacity constraint (in demand units)
    :constraints:                   named tuple of "dist_constraint" (int) to
                                    use as distance upper bound
                                    "soft_dist_constraint" (int) for soft
                                    upper bound constraint for vehicle
                                    distances "soft_dist_penalty" (int) for
                                    soft upper bound penalty for exceeding
                                    distance constraint
    :max_search_seconds:            int of solve time

    TODO:
    [ ] update with namedtuple usage
    [ ] use nodes list to handle as much as possible
    [ ] handle integer precision entirely
    [ ] refactor into smaller functions
    [ ] refactor with less arg complexity (better arg and config management)
    [ ] add solution type

    """
    num_nodes = len(nodes)

    if len(distance_matrix) - 1 == len(demand):
        demand = [0] + list(demand)

    # TODO: define a vehicle better
    num_vehicles = len(vehicle_caps)
    # TODO: can make these per vehicle
    distance_constraint = constraints.dist_constraint
    soft_distance_constraint = constraints.soft_dist_constraint
    soft_distance_penalty = constraints.soft_dist_penalty

    manager = pywrapcp.RoutingIndexManager(num_nodes, num_vehicles, depot_index)

    def matrix_callback(i: int, j: int):
        """index of from (i) and to (j)"""
        node_i = manager.IndexToNode(i)
        node_j = manager.IndexToNode(j)
        distance = distance_matrix[node_i][node_j]

        return distance

    def demand_callback(i: int):
        """capacity constraint"""
        _demand = demand[manager.IndexToNode(i)]

        return _demand

    def time_callback(i: int, j: int):
        """Returns the travel time between the two nodes."""
        node_i = manager.IndexToNode(i)
        node_j = manager.IndexToNode(j)

        return time_matrix[node_i][node_j]

    model = pywrapcp.RoutingModel(manager)

    # demand constraint setup
    model.AddDimensionWithVehicleCapacity(
        # function which return the load at each location (cf. cvrp.py example)
        model.RegisterUnaryTransitCallback(demand_callback),
        0,  # null capacity slack
        vehicle_caps,  # vehicle maximum capacity
        True,  # start cumul to zero
        "Capacity",
    )

    # distance constraints
    dist_callback_index = model.RegisterTransitCallback(matrix_callback)
    model.SetArcCostEvaluatorOfAllVehicles(dist_callback_index)
    model.AddDimensionWithVehicleCapacity(
        dist_callback_index,
        0,  # 0 slack
        [distance_constraint for i in range(num_vehicles)],
        True,  # start to zero
        "Distance",
    )

    dst_dim = model.GetDimensionOrDie("Distance")
    for i in range(manager.GetNumberOfVehicles()):
        end_idx = model.End(i)
        dst_dim.SetCumulVarSoftUpperBound(
            end_idx, soft_distance_constraint, soft_distance_penalty
        )

    # time windows constraint
    transit_callback_index = model.RegisterTransitCallback(time_callback)
    model.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
    model.AddDimension(
        transit_callback_index,
        30,  # allow waiting time
        30,  # maximum time per vehicle
        False,  # Don't force start cumul to zero.
        "Time",
    )

    time_dimension = model.GetDimensionOrDie("Time")
    # Add time window constraints for each location except depot.
    for location_idx, time_window in enumerate(time_windows):
        if location_idx == 0:
            continue
        index = manager.NodeToIndex(location_idx)
        time_dimension.CumulVar(index).SetRange(time_window[0], time_window[1])

    # Add time window constraints for each vehicle start node.
    for vehicle_id in range(num_vehicles):
        index = model.Start(vehicle_id)
        time_dimension.CumulVar(index).SetRange(time_windows[0][0], time_windows[0][1])

    for i in range(num_vehicles):
        model.AddVariableMinimizedByFinalizer(time_dimension.CumulVar(model.Start(i)))
        model.AddVariableMinimizedByFinalizer(time_dimension.CumulVar(model.End(i)))

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )
    search_parameters.time_limit.seconds = max_search_seconds

    assignment = model.SolveWithParameters(search_parameters)

    if assignment:
        Stop = namedtuple("Stop", ["idx", "lat", "lon", "demand", "dist"])

        solution = []
        for _route_number in range(model.vehicles()):
            route = []
            idx = model.Start(_route_number)

            if model.IsEnd(assignment.Value(model.NextVar(idx))):
                continue

            else:
                prev_node_index = manager.IndexToNode(idx)

                while True:
                    # TODO: time_var = time_dimension.CumulVar(order)
                    node_index = manager.IndexToNode(idx)
                    original_idx = nodes[node_index]["idx"]
                    lat = nodes[node_index]["lat"]
                    lon = nodes[node_index]["lon"]

                    d = demand[node_index]
                    dist = distance_matrix[prev_node_index][node_index]

                    route.append(Stop(original_idx, lat, lon, d, dist))

                    if model.IsEnd(idx):
                        break

                    prev_node_index = node_index
                    idx = assignment.Value(model.NextVar(idx))

            solution.append(route)

        return solution


def create_vehicles(
    origin_lat: float,
    origin_lon: float,
    dest_lats: List[float],
    dest_lons: List[float],
    demand_quantities: List[int],
    max_vehicle_capacity: int = 26,
) -> dict:  # TODO: tune in ortools-pyinteractive
    # demand including origin (ortools required)
    if len(demand_quantities) == len(dest_lats):
        all_demand = [0] + demand_quantities
    else:
        all_demand = demand_quantities

    # ad-hoc dynamic solve time TODO: utilize unique clusters and sizes, etc.
    if len(all_demand) - 1 > 250:
        max_search_seconds = 120
    elif len(all_demand) - 1 > 200 and len(all_demand) - 1 <= 250:
        max_search_seconds = 60
    elif len(all_demand) - 1 > 150 and len(all_demand) - 1 <= 200:
        max_search_seconds = 30
    else:
        max_search_seconds = 5

    int_precision = 100
    max_vehicle_dist = 3500 * int_precision
    max_vehicle_cap = max_vehicle_capacity
    num_vehicles = len(all_demand)
    soft_max_vehicle_dist = int(max_vehicle_dist * 0.75)
    soft_max_vehicle_cost = max_vehicle_dist + 1  # cost feels ambiguous

    vehicle_capacities = [max_vehicle_cap for i in range(num_vehicles)]

    distance_matrix = distance.create_matrix(
        origin_lat=origin_lat,
        origin_lon=origin_lon,
        dest_lats=dest_lats,
        dest_lons=dest_lons,
        int_precision=int_precision,
    )

    time_matrix = (np.array(distance_matrix) / 440 / int_precision).round(0).astype(int)
    time_windows = [(0, 23)] * len(distance_matrix)

    clusters = cluster.create_dbscan_clusters(lats=dest_lats, lons=dest_lons)

    Constraints = namedtuple(
        "Constraint",
        ["dist_constraint", "soft_dist_constraint", "soft_dist_penalty"],
    )
    constraints = Constraints(
        dist_constraint=max_vehicle_dist,
        soft_dist_constraint=soft_max_vehicle_dist,
        soft_dist_penalty=soft_max_vehicle_cost,
    )

    nodes_arr = np.array(
        [(0, origin_lat, origin_lon)]
        + list(zip(list(range(1, len(all_demand) + 1)), dest_lats, dest_lons)),
        dtype=[("idx", int), ("lat", float), ("lon", float)],
    )

    distance_matrix_arr = np.array(distance_matrix)
    windows_matrix_arr = np.array(time_matrix)
    windows_arr = np.array(time_windows, dtype=object)
    demand_arr = np.array(all_demand)
    vehicle_cap_arr = np.array(vehicle_capacities)

    # preprocess exceptions based on MAX_VEHICLE_DIST
    exceptions = np.where(distance_matrix_arr[0] > max_vehicle_dist)

    vehicle_count = 0
    vehicle_ids = [None] * len(dest_lats)
    stop_nums = [None] * len(dest_lats)
    for c in np.unique(clusters):
        # align with matrix
        is_cluster = np.where(clusters == c)[0]
        is_cluster = is_cluster + 1
        is_cluster = np.insert(is_cluster, 0, 0)
        is_cluster = is_cluster[~np.isin(is_cluster, exceptions)]

        solution = solve(
            nodes=nodes_arr[is_cluster],
            distance_matrix=distance_matrix_arr[is_cluster],
            time_matrix=windows_matrix_arr[is_cluster],
            time_windows=windows_arr[is_cluster],
            demand=demand_arr[is_cluster],
            vehicle_caps=vehicle_cap_arr[is_cluster],
            depot_index=0,
            constraints=constraints,
            max_search_seconds=max_search_seconds,
        )

        if not solution:
            continue

        for vehicle in solution:
            vehicle_count += 1

            for n, stop in enumerate(vehicle):
                if stop.idx != 0:
                    vehicle_ids[stop.idx - 1] = vehicle_count
                    stop_nums[stop.idx - 1] = n

    return {"id": vehicle_ids, "stops": stop_nums}
