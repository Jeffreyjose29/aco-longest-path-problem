import os
import numpy as np

class Node:
    def __init__(self, v, w, pheromone=0):
        self.v = v
        self.w = w
        self.pheromone = 0

    def __str__(self):
        return 'Node {} with weight {} and pheromone {}'.format(self.v,
            self.w, self.pheromone)

# def build_graph_from_file(graph_path, nb_vertex):
#     if not os.path.exists(graph_path):
#         exit('Error: Dataset {} not found'.format(graph_path))

#     graph = [{} for _ in range(nb_vertex)]
#     with open(graph_path, 'r') as fhandle:
#         for line in fhandle:
#             x, y, z = line[:-1].split(sep='\t')
#             x = int(x) - 1
#             y = int(y) - 1
#             graph[x][y] = Node(y, int(z))

#     return graph

def build_graph_from_file(graph_path, nb_vertex):
    if not os.path.exists(graph_path):
        exit('Error: Dataset {} not found'.format(graph_path))

    graph = np.zeros((nb_vertex,nb_vertex))
    identity = np.zeros((nb_vertex, nb_vertex))
    with open(graph_path, 'r') as fhandle:
        for line in fhandle:
            x, y, z = line[:-1].split(sep='\t')
            x = int(x) - 1
            y = int(y) - 1
            graph[x][y] = int(z)
            identity[x][y] = 1

    return graph, identity

def print_graph(graph):
    for i in range(len(graph)):
        print('Vertex {}'.format(i))
        for key, node in graph[i].items():
            print(node)
    print()