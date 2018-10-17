import copy

from aco.Ant import Ant
from aco.graph.Node import print_graph

class ACO():
    def __init__(self, graph, max_iterations, nb_ants, init_pheromone, evaporation, alpha, beta, rng):
        self.graph = copy.deepcopy(graph)
        self.max_iterations = max_iterations
        self.nb_ants = nb_ants
        self.init_pheromone = init_pheromone
        self.evaporation = evaporation
        self.alpha = alpha
        self.beta = beta
        self.rng = rng

        # Init Ants
        self.ants = [ Ant(end_vertex=len(graph)-1, alpha=self.alpha, beta=self.beta) for _ in range(self.nb_ants) ]

        # Init Pheromone
        for vertex in graph:
            for key, node in vertex.items():
                node.pheromone = self.init_pheromone

        # Best Solution
        self.best_solution = {
            'path': [],
            'cost': -1
        }

    def _update_phoromoe_trail(self, graph, ants):
        best_solution = self.best_solution

        for vertex in graph:
            # print(vertex)
            for key, node in vertex.items():
                node.pheromone = max(self.init_pheromone, node.pheromone * (1.0 - self.evaporation))

        for ant in self.ants:
            solution = ant.latest_solution
            if (solution):
                for i in range (0, len(solution['path'])-1):
                    # print('Updating path from {} to {}'.format(solution['path'][i], solution['path'][i+1]))
                    node = graph[solution['path'][i]][solution['path'][i+1]]
                    # print('updating by', self.evaporation * (1 - (1.0/solution['cost'])))
                    node.pheromone += self.evaporation * (1 - (1.0/solution['cost']))
        
        # print_graph(graph)
        # input()

    def run(self):
        for iteration in range(self.max_iterations):
            # print(iteration)
            for ant in self.ants:
                solution = ant.build_solution(self.graph, self.rng)
                
                # If it is a valid solution
                if (solution):
                    if (solution['cost'] > self.best_solution['cost']):
                        self.best_solution = solution


            # Update pheromone trail
            self._update_phoromoe_trail(self.graph, self.ants)
        
        print(self.best_solution['cost'])