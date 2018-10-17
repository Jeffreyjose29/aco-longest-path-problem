import numpy as np

class Ant():
    def __init__(self, end_vertex, alpha, beta, start_vertex=0):
        self.path = []
        self.end_vertex = end_vertex
        self.alpha = alpha
        self.beta = beta
        self.start_vertex = start_vertex

        self.last_solution = None

    def build_solution(self, graph, pheromone, rng, it):
        solution = {
            'path': [ self.start_vertex ],
            'cost': 0
        }

        # Build Solution
        cur_vertex = self.start_vertex
        
        visited_vertex = np.ones(graph.shape[0])
        # print(visited_vertex)
        
        while(cur_vertex != self.end_vertex):
            visited_vertex[cur_vertex] = 0

            possible_paths = graph[cur_vertex,:] * visited_vertex
            # print(possible_paths)
            # input('possible_paths')

            # Cant go anywhere else
            if ( np.sum(possible_paths) == 0 ):
                break
            
            p = np.power(pheromone[cur_vertex,:] * visited_vertex, self.alpha)
            w = np.power(possible_paths, self.beta)
            probs = p * w
            probs /= np.dot(p,w)

            # print(probs)
            # input('stop point')

            # print(probs)
            choice = rng.choice(len(probs), p=probs)
            # print(choice)
            # input('choice')
            next_vertex = choice

            solution['path'].append(choice)
            solution['cost'] += graph[cur_vertex][next_vertex]
            
            cur_vertex = choice

        if (cur_vertex != self.end_vertex):
            # print('Warning: Ant did not reach end')
            # print('Solution:', solution)
            solution = None

        self.latest_solution = solution

        return solution