import copy, time

import numpy as np

from aco.Ant import Ant
from aco.graph.Node import print_graph

import matplotlib.pyplot as plt
import networkx as nx

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

        G = nx.from_numpy_matrix(self.graph * self.pheromone, create_using=nx.MultiGraph)
        self.pos=nx.spring_layout(G)


    def _update_phoromoe_trail(self, graph, ants):
        best_solution = self.best_solution

        # evaporator = lambda x: if (x == 0): 0 else np.max(x, x * (1.0 - self.evaporation))
        # print(self.pheromone)
        # input('pheromone')
        self.pheromone = self.pheromone * (1.0 - self.evaporation) + (self.base_pheromone * 0.1)
        # self.pheromone = self.pheromone * (1.0 - self.evaporation) + self.base_pheromone
        # self.pheromone = np.maximum(self.pheromone, self.base_pheromone)
        # print(self.pheromone)
        # input('pheromone')

        ants = sorted(ants, key=lambda x: x.latest_solution['cost'] if (x.latest_solution) else -1, reverse=True)
        
        k = 15
        for count, ant in enumerate(ants):
            if(count+1 == k):
                break

            solution = ant.latest_solution
            # path_vector = np.zeros(graph.shape[0])
            # path_vector[solution['path']] = 1
            # print(path_vector)

            # self.pheromone[:]

            if (solution):
                for i in range (0, len(solution['path'])-1):
                    self.pheromone[solution['path'][i]][solution['path'][i+1]] += (1.0 - (1.0/solution['cost']))
        
        # for i in range (0, len(best_solution['path'])-1):
        #     self.pheromone[best_solution['path'][i]][best_solution['path'][i+1]] += self.evaporation * (1.0 - (1.0/best_solution['cost']))

        # G = nx.from_numpy_matrix(self.pheromone, create_using=nx.MultiGraph)

        # elarge=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] >0.5]
        # esmall=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] <=0.5]
        # nx.draw_networkx_edges(G,self.pos,edgelist=elarge, width=2)
        # nx.draw_networkx_edges(G,self.pos,edgelist=esmall, width=2, alpha=0.5,edge_color='b',style='dashed')

        # nx.draw(G, pos=self.pos,with_labels=True)
        # plt.show()


    def run(self):
        
        all_solutions = {}

        for iteration in range(self.max_iterations):
            all_solutions['Iteration ' + str(iteration)] = {
                'costs': []
            }

            start = time.time()
            for ant in self.ants:
                current_solution = ant.build_solution(self.graph, self.pheromone, self.rng, iteration)
                
                # If it is a valid solution
                if (current_solution):
                    all_solutions['Iteration ' + str(iteration)]['costs'].append(current_solution['cost'])
                    if (current_solution['cost'] > self.best_solution['cost']):
                        self.best_solution = current_solution
            # print('took ants seconds', time.time()-start)

            # Update pheromone trail
            start = time.time()
            self._update_phoromoe_trail(self.graph, self.ants)
            # print('took update seconds', time.time()-start)
        
            # print(iteration)
            if (iteration % 100 == 0):
                print('Iteration {} - Best Cost: {} - Mean/Std: {} +- {}'.format(iteration, 
                    self.best_solution['cost'], np.mean(all_solutions['Iteration ' + str(iteration)]['costs']),
                    np.std(all_solutions['Iteration ' + str(iteration)]['costs'])))

        print(self.best_solution)
        # input()
        return all_solutions, self.best_solution 