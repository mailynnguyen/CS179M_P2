import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from itertools import permutations
import math
import time

# euclidean distance
def distance(p1, p2):
    return np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def total_path_distance(points, order): # points is the list of points in the cluster, order is the order of the points taken
    dist = 0
    for i in range(len(order)-1): # going 1 less because using order[i+1]
        dist += distance(points[order[i]], points[order[i+1]])
    dist += distance(points[order[-1]], points[order[0]])  # return to pad
    return dist

def nearest_neighbor_route(points):
    n = len(points)
    unvisited = list(range(1, n)) # this will be used to index in points array
    route = [0] # starting node, visited nodes
    while unvisited:
        last = route[-1] # make last the last node in route
        next_city = min(unvisited, key=lambda j: distance(points[last], points[j])) # j is from unvisited # takes all points in univisted and compares against last
        route.append(next_city) # add the visted node to route 
        unvisited.remove(next_city) # remove it from unvisited
    return route, total_path_distance(points, route)

def compute_routes(file_name):
    data = np.loadtxt(file_name)
    print(f"ComputePossibleSolutions\nEnter the name of file: {file_name}")
    print(f"There are {len(data)} nodes: Solutions will be available in 5 minutes or less\n")
    
    for k in range(1, 5):  # 1 to 4 drones
        if k == 1:
            cluster_centers = [np.mean(data, axis=0)]
            labels = np.zeros(len(data))
        else:
            kmeans = KMeans(n_clusters=k, n_init=10, random_state=42).fit(data)
            labels = kmeans.labels_
            cluster_centers = kmeans.cluster_centers_

        total_distance = 0
        print(f"If you use {k} drone(s):")

        for i in range(k):
            cluster_points = data[labels == i] # select only the rows from data whose corresponding labels value equals i
            route, route_dist = nearest_neighbor_route(cluster_points)
            pad = np.mean(cluster_points, axis=0)
            if route_dist > total_distance:
                    total_distance = route_dist
            # total_distance += route_dist
            print(f" Landing Pad {i+1} should be at {pad.round(2)}, "
                  f"serving {len(cluster_points)} locations, route is {route_dist:.1f} meters")

        flight_time = total_distance / 100  # drones move 100 m/min
        setup_time = 2 * k
        print(f" Total route distance = {total_distance:.1f} meters")
        print(f" Estimated time = {flight_time + setup_time:.1f} minutes\n")

if __name__ == "__main__":
    filename = input("Enter the filename (e.g. Almond9832.txt): ")
    start = time.time()
    compute_routes(filename)
    print(f"Execution completed in {time.time() - start:.2f} seconds.")