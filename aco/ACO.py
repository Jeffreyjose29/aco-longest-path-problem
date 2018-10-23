import copy, time

import numpy as np

from aco.Ant import Ant
from aco.graph.Node import print_graph

class ACO():
    def __init__(self, graph, identity, max_iterations, nb_ants, init_pheromone, evaporation, alpha, beta, rng):
        self.graph = copy.copy(graph)
        self.identity = copy.copy(identity)
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
        self.pheromone = identity * init_pheromone
        self.base_pheromone = copy.copy(self.pheromone)

        # Best Solution
        self.best_solution = {
            'path': [],
            'cost': 0
        }


    def _update_phoromoe_trail(self, graph, ants):
        # Evaporate pheromone
        self.pheromone = self.pheromone * (1.0 - self.evaporation) + (self.base_pheromone * 0.1)

        # Sort ants by best cost
        ants = sorted(ants, key=lambda x: x.latest_solution['cost'] if (x.latest_solution) else -1, reverse=True)
        
        k = self.nb_ants * 0.5
        for count, ant in enumerate(ants):
            if(count+1 >= k):
                break

            solution = ant.latest_solution

            # If valid Solution, add pheromone to trail
            if (solution):
                for i in range (0, len(solution['path'])-1):
                    self.pheromone[solution['path'][i]][solution['path'][i+1]] += (1.0 - (1.0/solution['cost']))


    def run(self):
        
        all_solutions = {}

        for iteration in range(self.max_iterations):
            all_solutions['Iteration ' + str(iteration)] = {
                'costs': [],
                'best_cost': []
            }

            for ant in self.ants:
                # Build Solution
                current_solution = ant.build_solution(self.graph, self.pheromone, self.rng, iteration)
                
                # If it is a valid solution
                if (current_solution):
                    all_solutions['Iteration ' + str(iteration)]['costs'].append(current_solution['cost'])
                    if (current_solution['cost'] > self.best_solution['cost']):
                        self.best_solution = current_solution

            all_solutions['Iteration ' + str(iteration)]['best_cost'] = self.best_solution['cost']

            # Update pheromone trail
            self._update_phoromoe_trail(self.graph, self.ants)
        
            # print(iteration)
            if (iteration % 100 == 0):
                print('Iteration {} - Best Cost: {} - Mean/Std: {} +- {}'.format(iteration, 
                    self.best_solution['cost'], np.mean(all_solutions['Iteration ' + str(iteration)]['costs']),
                    np.std(all_solutions['Iteration ' + str(iteration)]['costs'])))

        print('Best Solution:', self.best_solution)

        return all_solutions, self.best_solution 