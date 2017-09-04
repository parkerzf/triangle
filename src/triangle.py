import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
from math import sqrt
import networkx as nx
import heapq as hq



def dist(idx1, idx2, points):
	point1 = points[idx1]
	point2 = points[idx2]
	return sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

csvfile = sys.argv[1]
name = sys.argv[2]
threshold = float(sys.argv[3])

plt.figure(figsize=(10,10))


points = np.genfromtxt(csvfile, dtype=None, delimiter='\t')
points = points * 3
tri = Delaunay(points)
plt.triplot(points[:,0], points[:,1], tri.simplices.copy())
plt.plot(points[:,0], points[:,1], 'o')
#change the first point to another shape
plt.plot(points[0,0], points[0,1], 'D')
plt.savefig('planar.png')

num_nodes = len(points)
g=nx.Graph()


planar_matrix = np.zeros(shape=(points.shape[0], points.shape[0]))


for triangle in tri.simplices:
	a = triangle[0]
	b = triangle[1]
	c = triangle[2]

	if planar_matrix[a,b] == 0.:
		distance = dist(a,b,points)
		planar_matrix[a,b] = distance
		planar_matrix[b,a] = distance
		g.add_edge(a, b, weight=distance)

	if planar_matrix[a,c] == 0.:
		distance = dist(a,c,points)
		planar_matrix[a,c] = distance
		planar_matrix[c,a] = distance
		g.add_edge(a, c, weight=distance)

	if planar_matrix[b,c] == 0.:
		distance = dist(b,c,points)
		planar_matrix[b,c] = distance
		planar_matrix[c,b] = distance
		g.add_edge(b, c, weight=distance)

np.savetxt('planar_matrix.csv', planar_matrix, delimiter=',', fmt='%.1f')

path_graph = nx.minimum_spanning_tree(g)

print("# nodes: " + str(g.number_of_nodes()))

pos_dict = {}
for node in g.nodes():
	pos_dict[node] = points[node]
	path_graph.node[node]['x'] = float(points[node][0])
	path_graph.node[node]['y'] = float(points[node][1])

plt.clf()
plt.plot(points[:,0], points[:,1], 'o')
#change the first point to another shape
plt.plot(points[0,0], points[0,1], 'D')
nx.draw_networkx_edges(path_graph, pos = pos_dict, width=3, edge_color='r')
plt.savefig("mst.png")


all_shortest_path_length_dict = nx.shortest_path_length(g, weight = "weight")


min = float("inf")
min_start = -1
min_end = -1
max = 0
max_end = -1
max_end = -1

for i in range(0, num_nodes):
	for j in range(i+1, num_nodes):
		if all_shortest_path_length_dict[i][j] < min:
			min = all_shortest_path_length_dict[i][j]
			min_start = i
			min_end = j
		if all_shortest_path_length_dict[i][j] > max:
			max = all_shortest_path_length_dict[i][j]
			max_start = i
			max_end = j
		
print ("min shortest path: " + str(min_start) + "->" + str(min_end) + ", " + str(min))
print ("max shortest path: " + str(max_start) + "->" + str(max_end) + ", " + str(max))

direct_matrix = np.zeros(shape=(points.shape[0], points.shape[0]))

for i in range(0, points.shape[0]):
	for j in range(0, points.shape[0]):
		direct_matrix[i,j] = dist(i,j,points)


np.savetxt('direct_matrix.csv', direct_matrix, delimiter=',', fmt='%.1f')

threshold_graph = nx.Graph()


while True:
	# Calculate the shortest path distance SP
	SP_matrix = nx.shortest_path_length(path_graph, weight = "weight")
	heap = []
	for i in range(0, points.shape[0]):
		for j in range(0, points.shape[0]):
			if i != j:
				# Calculate ratio = d/SP
				# Sort ratio in a nondecreasing order
				ratio = direct_matrix[i,j]/SP_matrix[i][j]
				if ratio < 1.0:
					hq.heappush(heap, (ratio, i, j))
	# Pick the first node pair on the list, connect them with an edge
	min_ratio, x, y = hq.heappop(heap)
	print 'min_ratio', min_ratio
	# Stop when min_ratio >= threshold
	if min_ratio >= threshold:
		break
	# Update the graph
	path_graph.add_edge(x, y, weight = float(direct_matrix[x,y]))
	threshold_graph.add_edge(x, y, weight = direct_matrix[x,y])
	

# plt.clf()
plt.plot(points[:,0], points[:,1], 'o')
#change the first point to another shape
plt.plot(points[0,0], points[0,1], 'D')
nx.draw_networkx_edges(threshold_graph, pos = pos_dict, width=3, edge_color='b')
plt.savefig("threshold_"+ name + "_" + str(threshold) + ".png")

nx.write_graphml(path_graph, "threshold_"+ name + "_" + str(threshold) + ".graphml")

SP_matrix = nx.shortest_path_length(path_graph, weight = "weight")
