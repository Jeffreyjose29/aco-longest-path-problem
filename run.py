import argparse, time, os

from aco.utils import build_graph_from_file

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
    parser.add_argument('--iterations', '-i', type=int, default=20,
                        help='Number of iterations')
    parser.add_argument('--evaporation', '-e', type=float, default=0.1,
                        help='Evaporation rate')

    # Special Arguments
    parser.add_argument('--cores', '-c', type=int, default=6,
                        help='Number of cores')
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
    
