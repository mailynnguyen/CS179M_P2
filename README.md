# CS179M_P2
This algorithm receives an input of coordinates. These coordinates are clustered up in groups. The algorithm runs the K-Means algorithm to find the center of these clusters. Once the algorithm has determined how many clusters there are and the center of these clusters, the algorithm "places drones in the center of the clusters" and uses the greedy nearest neighbor algorithm to find the shortest route through all the points in the cluster. The algorithm gives outputs for if the all the points were clustered in 1 to 4 groups.

## Instructions
To Run: 
  1. Run the file `ComputePossibleSolutions.py` in the terminal in the project directory 
  2. Enter the fille such as `Almond9832.txt`, input files are included 
