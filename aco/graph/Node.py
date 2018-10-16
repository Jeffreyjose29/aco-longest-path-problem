class Node:
    def __init__(self, v, w, pheromone=0):
        self.v = v
        self.w = w
        self.pheromone = 0

    def __str__(self):
        return 'Node {} with weight {} and pheromone {}'.format(self.v,
            self.w, self.pheromone)