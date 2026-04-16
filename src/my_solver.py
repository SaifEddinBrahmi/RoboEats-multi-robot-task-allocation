import numpy as np
from itertools import permutations, combinations

KITCHEN_R1 = [7, 1.75]
KITCHEN_R2 = [7, 1]

DELIVERY_POINTS = {
    1: [3.25, 2],
    2: [3.25, 5],
    3: [3.25, 8],
    4: [3.25, 11],
    5: [7.25, 5],
    6: [7.25, 8],
    7: [7.25, 11],
    8: [8.75, 5],
    9: [8.75, 8],
    10: [8.75, 11]
}


def distance(p1, p2):
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def route_distance(start, tables, end):
    if not tables:
        return 0
    points = [DELIVERY_POINTS[t] for t in tables]
    total = distance(start, points[0])
    for i in range(len(points) - 1):
        total += distance(points[i], points[i + 1])
    total += distance(points[-1], end)
    return total


def solve_tsp(start, tables, end):
    if not tables:
        return [], 0
    if len(tables) == 1:
        return tables, route_distance(start, tables, end)
    
    best_order = None
    best_dist = float('inf')
    
    for perm in permutations(tables):
        d = route_distance(start, list(perm), end)
        if d < best_dist:
            best_dist = d
            best_order = list(perm)
    
    return best_order, best_dist


def estimate_time(dist_r1, dist_r2):
    speed = 1.2
    time_r1 = dist_r1 / speed if dist_r1 > 0 else 0
    time_r2 = dist_r2 / speed if dist_r2 > 0 else 0
    return max(time_r1, time_r2) if max(time_r1, time_r2) > 0 else 0.001


def find_optimal_allocation(tables):
    n = len(tables)
    best_metric = float('inf')
    best_allocation = ([], [])
    best_routes = ([], [])
    
    if n == 1:
        t = tables[0]
        d1 = distance(KITCHEN_R1, DELIVERY_POINTS[t])
        d2 = distance(KITCHEN_R2, DELIVERY_POINTS[t])
        if d1 <= d2:
            return ([t], []), ([t], [])
        else:
            return ([], [t]), ([], [t])
    
    for r in range(n + 1):
        for r1_tables in combinations(tables, r):
            r1_tables = list(r1_tables)
            r2_tables = [t for t in tables if t not in r1_tables]
            
            route_r1, dist_r1 = solve_tsp(KITCHEN_R1, r1_tables, KITCHEN_R1)
            route_r2, dist_r2 = solve_tsp(KITCHEN_R2, r2_tables, KITCHEN_R2)
            
            total_dist = dist_r1 + dist_r2
            time = estimate_time(dist_r1, dist_r2)
            metric = total_dist * time
            
            if metric < best_metric:
                best_metric = metric
                best_allocation = (r1_tables, r2_tables)
                best_routes = (route_r1, route_r2)
    
    return best_allocation, best_routes


def find_balanced_allocation(tables):
    left_tables = []
    right_tables = []
    
    for t in tables:
        if DELIVERY_POINTS[t][0] < 5:
            left_tables.append(t)
        else:
            right_tables.append(t)
    
    route_r1, dist_r1 = solve_tsp(KITCHEN_R1, right_tables, KITCHEN_R1)
    route_r2, dist_r2 = solve_tsp(KITCHEN_R2, left_tables, KITCHEN_R2)
    
    return (right_tables, left_tables), (route_r1, route_r2), (dist_r1, dist_r2)


def call(tables_to_serve):
    # try both strategies
    (tables_r1_opt, tables_r2_opt), (route_r1_opt, route_r2_opt) = find_optimal_allocation(tables_to_serve)
    dist_r1_opt = route_distance(KITCHEN_R1, route_r1_opt, KITCHEN_R1)
    dist_r2_opt = route_distance(KITCHEN_R2, route_r2_opt, KITCHEN_R2)
    
    (tables_r1_bal, tables_r2_bal), (route_r1_bal, route_r2_bal), (dist_r1_bal, dist_r2_bal) = find_balanced_allocation(tables_to_serve)
    
    # prefer using both robots for parallel execution
    if len(tables_to_serve) >= 2 and len(route_r1_bal) > 0 and len(route_r2_bal) > 0:
        route_r1, route_r2 = route_r1_bal, route_r2_bal
        dist_r1, dist_r2 = dist_r1_bal, dist_r2_bal
    else:
        route_r1, route_r2 = route_r1_opt, route_r2_opt
        dist_r1, dist_r2 = dist_r1_opt, dist_r2_opt
    
    waypoints_R1 = [DELIVERY_POINTS[t] for t in route_r1]
    waypoints_R2 = [DELIVERY_POINTS[t] for t in route_r2]
    
    if(waypoints_R1):
        waypoints_R1.append([7,2.5])
    # R1 goes down on right side (avoid chairs)
    if(waypoints_R2):
        waypoints_R2.append([4,0.5])
        waypoints_R2.append([5,0.5])
        waypoints_R2.append([6,0.5])
           # R2 goes down on left side (avoid chairs)
    
    waypoints_R1.append(KITCHEN_R1)
    waypoints_R2.append(KITCHEN_R2)
    
    print(f"R1: {route_r1} ({dist_r1:.2f}m) | R2: {route_r2} ({dist_r2:.2f}m)")
    
    return waypoints_R1, waypoints_R2
