import argparse, time, os, json, copy

import numpy as np
import multiprocessing as mp

from aco.ACO import ACO
from aco.graph.Node import build_graph_from_file

np.set_printoptions(suppress=True)

def aco_run(runs_solutions, runs_best_solutions, graph, identity, args, seed):
    rng = np.random.RandomState(seed=seed)
    aco = ACO(graph, identity, args.iterations, args.ants, args.init_pheromone,
            args.evaporation, args.alpha, args.beta, rng)
    solutions, best_solution = aco.run()

    runs_solutions.append(solutions)
    runs_best_solutions.append(best_solution)

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
    parser.add_argument('--alpha', type=float, default=1.0)
    parser.add_argument('--beta', type=float, default=1.0)

    # Special Arguments
    parser.add_argument('--jobs', '-j', type=int, default=6)
    parser.add_argument('--random-seed', type=int, default=481516)
    parser.add_argument('--save-dir', type=str, default=str(time.time()).split('.')[0],
                        help='The save directory. Experiments will be saved on experiments/$SAVE_DIR/$SUB_DIR')
    parser.add_argument('--sub-dir', type=str, default='all',
                        help='The save directory. Experiments will be saved on experiments/$SAVE_DIR/$SUB_DIR')

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
    graph, identity = build_graph_from_file(graph_path, nb_vertex)

    # Seeds to be used across all runs
    rgenerator = np.random.RandomState(seed=args.random_seed)
    run_seeds = rgenerator.randint(0, 1000000000, args.runs)

    run_solutions = {
        'Parameters': {
            'Iterations': args.iterations,
            'Ants': args.ants,
            'Initial Pheromone': args.init_pheromone,
            'Evaporation': args.evaporation,
            'Alpha': args.alpha,
            'Beta': args.beta
        },
        'Runs': [],
    }
    run_best_solutions = copy.deepcopy(run_solutions)

    # Normal run, for debugging
    # for i in range(0, args.runs):
    #     new_rng = np.random.RandomState(seed=run_seeds[i])
    #     aco = ACO(graph, identity, args.iterations, args.ants, args.init_pheromone,
    #         args.evaporation, args.alpha, args.beta, new_rng)
    #     solutions, best_solution = aco.run()

    #     run_solutions['Runs'].append(solutions)
    #     run_best_solutions['Runs'].append(best_solution)

    # Parallel Run
    pool = mp.Pool(args.jobs)
    processes = []
    with mp.Manager() as manager:
        runs_solutions = manager.list()
        runs_best_solutions = manager.list()
        for i in range(0, args.runs):
            pool.apply_async(aco_run,
                args=(runs_solutions, runs_best_solutions, graph, identity, args, run_seeds[i]))
        pool.close()
        pool.join()
        
        run_solutions['Runs'] = list(runs_solutions)
        run_best_solutions['Runs'] = list(runs_best_solutions)

    # Compute Mean and STD for Best solutions
    cost_best_solutions = [ x['cost'] for x in run_best_solutions['Runs'] ]
    max_cost = -1
    max_cost_path = None
    for x in run_best_solutions['Runs']:
        if (x['cost'] > max_cost):
            max_cost = x['cost']
            max_cost_path = x['path']
    stats = 'Mean Best Solution: {} +- {}\nMax Cost: {}\nPath: {}'.format(np.mean(cost_best_solutions), np.std(cost_best_solutions), max_cost, max_cost_path)

    # Save Files
    save_file = 'it{}_ant{}_ipher{}_evap{}_alph{}_bet{}'.format(
        args.iterations,
        args.ants,
        args.init_pheromone,
        args.evaporation,
        args.alpha,
        args.beta
    )

    save_dir = os.path.join('experiments', args.save_dir, args.sub_dir)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    with open(os.path.join(save_dir, 'sol_' + save_file + '.json'), 'w') as fhandle:
        json.dump(run_solutions, fhandle, indent=2)
    with open(os.path.join(save_dir, 'best_sol_' + save_file + '.json'), 'w') as fhandle:
        json.dump(run_best_solutions, fhandle, indent=2)
    with open(os.path.join(save_dir, 'stats_' + save_file + '.txt'), 'w') as fhandle:
        fhandle.write(stats)

    print(os.path.join(save_dir, 'sol_' + save_file + '.json'))