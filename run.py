import argparse, time, os

import numpy as np

from aco.ACO import ACO
from aco.graph.Node import build_graph_from_file

if __name__ == '__main__':
    # Argument Parser
    parser = argparse.ArgumentParser(description='ACO - Longest Path Problem')

    # ACO Arguments
    parser.add_argument('--dataset', '-d', type=str, required=True,
                        choices=['graph1', 'graph2', 'graph3'],
                        help='Dataset to be used')
    parser.add_argument('--runs', '-r', type=int, default=10,
                        help='Number of runs to calculate mean and std')
    parser.add_argument('--ants', '-a', type=int, default=20,
                        help='Number of ants')
    parser.add_argument('--iterations', '-i', type=int, default=50)
    parser.add_argument('--evaporation', '-e', type=float, default=0.1)
    parser.add_argument('--init-pheromone', type=float, default=0.1)
    parser.add_argument('--alpha', type=float, default=1)
    parser.add_argument('--beta', type=float, default=2)

    # Special Arguments
    parser.add_argument('--jobs', '-j', type=int, default=6)
    parser.add_argument('--random-seed', type=int, default=481516)
    parser.add_argument('--save-dir', type=str, default=str(time.time()).split('.')[0],
                        help='The save directory. Experiments will be saved on experiments/$SAVE_DIR')

    args = parser.parse_args()
    print('Running with args:', args)

    # Load graph
    if (args.dataset == 'graph1'):
        nb_vertex = 100
    elif (args.dataset == 'graph2'):
        nb_vertex = 20
    elif (args.dataset == 'graph3'):
        nb_vertex = 1000
    graph_path = os.path.join('dataset', args.dataset + '.txt')
    graph = build_graph_from_file(graph_path, nb_vertex)

    # Seeds to be used across all runs
    rgenerator = np.random.RandomState(seed=args.random_seed)
    run_seeds = rgenerator.randint(0, 1000000000, args.runs)

    for i in range(0, args.runs):
        new_rng = np.random.RandomState(seed=run_seeds[i])
        aco = ACO(graph, args.iterations, args.ants, args.init_pheromone,
            args.evaporation, args.alpha, args.beta, new_rng)
        aco.run()