import copy

from aco.Ant import Ant

class ACO():
    def __init__(self, graph, max_iterations, nb_ants, init_pheromone, alpha, beta, rng):
        self.graph = copy.deepcopy(graph)
        self.max_iterations = max_iterations
        self.nb_ants = nb_ants
        self.init_pheromone = init_pheromone
        self.alpha = alpha
        self.beta = beta
        self.rng = rng

        # Init Ants
        self.ants = [ Ant(end_vertex=len(graph)-1, alpha=self.alpha, beta=self.beta) for _ in range(self.nb_ants) ]

        # Best Solution
        self.best_solution = {
            'path': [],
            'cost': -1
        }

    def _update_phoromoe_trail(self, graph):
        best_solution = self.best_solution

    def run(self):
        for iteration in range(self.max_iterations):
            for ant in self.ants:
                solution = ant.build_solution(self.graph, self.rng)
                
                # If it is a valid solution
                if (solution):
                    if (solution['cost'] > self.best_solution['cost']):
                        self.best_solution = solution


            # Update pheromone trail
            self._update_phoromoe_trail(self.graph)
        
        print(self.best_solution)