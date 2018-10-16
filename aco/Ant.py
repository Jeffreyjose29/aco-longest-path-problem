import numpy as np

class Ant():
    def __init__(self, end_vertex, alpha, beta, start_vertex=0):
        self.path = []
        self.end_vertex = end_vertex
        self.alpha = alpha
        self.beta = beta
        self.start_vertex = start_vertex

    def build_solution(self, graph, rng):
        solution = {
            'path': [ self.start_vertex ],
            'cost': 0
        }

        # Build Solution
        cur_vertex = self.start_vertex
        visited_vertex = set()
        visited_vertex.add(cur_vertex)

        while(cur_vertex != self.end_vertex):
            possible_paths = []
            for key, vertex in graph[cur_vertex].items():
                if vertex.v not in visited_vertex:
                    possible_paths.append( vertex )

            # Cant go anywhere else
            if (len(possible_paths) == 0):
                break
            
            denominator = 0
            for vertex in possible_paths:
                denominator += vertex.pheromone**self.alpha + vertex.w**self.beta
            
            probs = []
            for vertex in possible_paths:
                probs.append( (vertex.pheromone**self.alpha + vertex.w**self.beta) / denominator)
            
            choice = rng.choice(len(possible_paths), p=probs)
            next_vertex = possible_paths[choice]

            solution['path'].append(next_vertex.v)
            solution['cost'] += next_vertex.w
            
            cur_vertex = next_vertex.v

        if (cur_vertex != self.end_vertex):
            print('Warning: Ant did not reach end')
            print('Solution:', solution)
            solution = None

        return solution