import os

import numpy as np

from aco.graph.Node import Node

def build_graph_from_file(graph_path, nb_vertex):
    if not os.path.exists(graph_path):
        exit('Error: Dataset {} not found'.format(graph_path))

    graph = [[] for _ in range(nb_vertex)]
    with open(graph_path, 'r') as fhandle:
        for line in fhandle:
            x, y, z = line[:-1].split(sep='\t')
            x = int(x) - 1
            y = int(y) - 1
            graph[x].append(Node(y, int(z)))

    # for i in range(len(graph)):
    #     print('Vertex {}'.format(i))
    #     for node in graph[i]:
    #         print(node)
    #     print()

    return graph