import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from itertools import permutations
import math
import time
import matplotlib.pyplot as plt

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
    
    clusters = []
    routes = []
    route_dists = []
    seK_Distances = {} #Initialize dictionary to hold sek values
    for k in range(1, 5):  # 1 to 4 drones
        seK_val = 0.0 #initialize the value for sek
        if k == 1:
            cluster_centers = [np.mean(data, axis=0)]
            labels = np.zeros(len(data))

            center = cluster_centers[0]
            seK_val = np.sum((data-center)**2) #This is because we need to find the sum of squared distances from the center
        else:
            kmeans = KMeans(n_clusters=k, n_init=10, random_state=42).fit(data)
            labels = kmeans.labels_
            cluster_centers = kmeans.cluster_centers_

            seK_val = kmeans.inertia_ # sum of squared distances to closest cluster center

        seK_Distances[f"Drone {k}"] = f"{seK_val:.2f}" #store sek score to dictionary
        total_distance = 0
        print(f"If you use {k} drone(s):")

        #print(f"Objective function (seK) = {seK_val:.2f}")
        for i in range(k):
            cluster_points = data[labels == i] # select only the rows from data whose corresponding labels value equals i
            route, route_dist = nearest_neighbor_route(cluster_points)
            clusters.append(cluster_points)
            routes.append(route)
            route_dists.append(route_dist)
            pad = np.mean(cluster_points, axis=0)
            if route_dist > total_distance:
                    total_distance = route_dist
            print(f" Landing Pad {i+1} should be at {pad.round(2)}, "
                  f"serving {len(cluster_points)} locations, route is {route_dist:.1f} meters")

        flight_time = total_distance / 100  # drones move 100 m/min
        setup_time = 2 * k
        print(f" Total route distance = {total_distance:.1f} meters")
        print(f" Estimated time = {flight_time + setup_time:.1f} minutes\n")
        
        #Print seK Dictionary
        #print("seK values for different number of drones:")
        #print(seK_Distances)
    
    return clusters, routes, route_dists
        
def create_output_files(input_file, num_drones, clusters, routes, route_dists):

    if num_drones == 1:
        clusters = clusters[0]
        routes = routes[0]
        route_dists = route_dists[0]
    elif num_drones == 2:
        clusters = clusters[1:3]
        routes = routes[1:3]
        route_dists = route_dists[1:3]
    elif num_drones == 3:
        clusters = clusters[3:6]
        routes = routes[3:6]
        route_dists = route_dists[3:6]  
    else:
        clusters = clusters[6:10]
        routes = routes[6:10]
        route_dists = route_dists[6:10]

    print("Writing ", end="")
    for i in range(num_drones):
        cluster_points = np.array(clusters[i]) # list of coordinates in the cluster, numpy makes it a 2d array
        ordered_points = cluster_points[routes[i]] # routes is list of indices in the cluster, advanced indexing
        with open(f"{input_file.replace('.txt', '')}_{i+1}_SOLUTION_{int(route_dists[i])}.txt", "w") as output_file:
            for x, y in ordered_points:
                output_file.write(f"{x:.7e} {y:.7e}\n")
        print(output_file.name, end=", ")
    print("to disk")

def create_visuals(input_file, num_drones, routes, clusters):

    if num_drones == 1:
        clusters = clusters[0]
        routes = routes[0]
    elif num_drones == 2:
        clusters = clusters[1:3]
        routes = routes[1:3]
    elif num_drones == 3:
        clusters = clusters[3:6]
        routes = routes[3:6]
    else:
        clusters = clusters[6:10]
        routes = routes[6:10]

    centers = []
    for i in range(num_drones):
        cluster_points = np.array(clusters[i])
        ordered_points = cluster_points[routes[i]]
        plt.scatter(cluster_points[:, 0], cluster_points[:, 1])
        plt.plot(ordered_points[:, 0], ordered_points[:, 1])

        centers.append(np.mean(cluster_points, axis=0))
    
    centers = np.array(centers)
    plt.scatter(centers[:, 0], centers[:, 1], marker='X')

    plt.savefig(f"{input_file.replace('.txt', '')}_OVERALL_SOLUTION.jpeg")
    plt.show()

if __name__ == "__main__":
    filename = input("Enter the filename (e.g. Almond9832.txt): ")
    start = time.time()
    clusters, routes, route_dists = compute_routes(filename)
    print(f"Execution completed in {time.time() - start:.2f} seconds.")
    num_drones = int(input("\n\nPlease select your choice 1 to 4: "))
    create_output_files(filename, num_drones, clusters, routes, route_dists)
    create_visuals(filename, num_drones, routes, clusters)