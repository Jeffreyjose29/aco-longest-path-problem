import os, json, argparse, pickle

import matplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt

import numpy as np

def find_lims(paths):
    ymin = 999999
    ymax = -1

    for _, path in enumerate(args.paths):
        with open(path, 'r') as fhandle:
            score = json.loads(fhandle.read())
        
        fitness_max = []
        fitness_min = []
        fitness_best = []
        for runs in score['Runs']:
            max_iteration = []
            min_iteration = []
            best_iteration = []
            for key, iteration in runs.items():
                max_iteration.append(np.max(iteration['costs']))
                min_iteration.append(np.min(iteration['costs']))
                best_iteration.append(iteration['best_cost'])
            fitness_max.append(max_iteration)
            fitness_min.append(min_iteration)
            fitness_best.append(best_iteration)
        
        ymin = min(ymin, np.min(fitness_min))
        ymax = max(ymax, max(np.max(fitness_best), np.max(fitness_max)))
    
    return ymin, ymax + 10

def save_table(figs, save_path):
    table = ('\\begin{{figure}}[ht]\n'
                '\t\\label{{fig7}}\n' 
                '\t\\begin{{minipage}}[b]{{0.5\\linewidth}}\n'
                '\t\t\\centering\n'
                '\t\t\\includegraphics[width=1\\linewidth]{{{}}}\n'
                '\t\t\\caption{{Initial condition}}\label{{fig:1}}\n'
                '\t\t\\vspace{{4ex}}\n'
                '\t\\end{{minipage}}%%\n'
                '\t\\begin{{minipage}}[b]{{0.5\\linewidth}}\n'
                '\t\t\\centering\n'
                '\t\t\\includegraphics[width=1\\linewidth]{{{}}}\n'
                '\t\t\\caption{{Rupture}}\label{{fig:2}}\n'
                '\t\t\\vspace{{4ex}}\n'
                '\t\\end{{minipage}}\n' 
                '\t\\begin{{minipage}}[b]{{0.5\\linewidth}}\n'
                '\t\t\\centering\n'
                '\t\t\\includegraphics[width=1\\linewidth]{{{}}}\n'
                '\t\t\\caption{{DFT, Initial condition}}\label{{fig:3}}\n'
                '\t\t\\vspace{{4ex}}\n'
                '\t\\end{{minipage}}%%\n' 
                '\t\\begin{{minipage}}[b]{{0.5\\linewidth}}\n'
                '\t\t\\centering\n'
                '\t\t\\includegraphics[width=1\\linewidth]{{{}}}\n'
                '\t\t\\caption{{DFT, rupture}}\label{{fig:4}}\n'
                '\t\t\\vspace{{4ex}}\n'
                '\t\\end{{minipage}}\n' 
                '\\end{{figure}}\n').format(figs[0], figs[1], figs[2], figs[3])
    
    with open(os.path.join(save_path, 'figure.txt'), 'w') as fhandle:
        fhandle.write(table)

# Argument Parser
parser = argparse.ArgumentParser(description='ACO - Longest Path Problem Plotter')

parser.add_argument('--paths', nargs='+', type=str, required=True)
parser.add_argument('--nth', type=int, default=10)
parser.add_argument('--yticks', type=int, default=100)

args = parser.parse_args()

plt.style.use('ggplot')

ymin, ymax = find_lims(args.paths)

figs = []
for index, path in enumerate(args.paths):
    f = plt.figure()
    f.set_figheight(5)
    f.set_figwidth(7)

    with open(path, 'r') as fhandle:
        score = json.loads(fhandle.read())

    fitness_avg = []
    fitness_max = []
    fitness_min = []
    fitness_best = []
    for runs in score['Runs']:
        avg_iteration = []
        max_iteration = []
        min_iteration = []
        best_iteration = []
        for key, iteration in runs.items():
            avg_iteration.append(np.mean(iteration['costs']))
            max_iteration.append(np.max(iteration['costs']))
            min_iteration.append(np.min(iteration['costs']))
            best_iteration.append(iteration['best_cost'])
        fitness_avg.append(avg_iteration)
        fitness_max.append(max_iteration)
        fitness_min.append(min_iteration)
        fitness_best.append(best_iteration)

    x_axis = np.arange(0,len(fitness_avg[0]))

    every_nth = args.nth

    plt.plot(x_axis[::every_nth], np.mean(fitness_best, axis=0)[::every_nth], c='tab:purple', label='Melhor Solução')
    plt.fill_between(x_axis[::every_nth],
                    np.mean(fitness_best, axis=0)[::every_nth] - np.std(fitness_best, axis=0)[::every_nth],
                    np.mean(fitness_best, axis=0)[::every_nth] + np.std(fitness_best, axis=0)[::every_nth],
                    alpha=0.3, color='tab:purple')

    plt.plot(x_axis[::every_nth], np.mean(fitness_avg, axis=0)[::every_nth], 'b-', label='Fitness Média')
    plt.fill_between(x_axis[::every_nth],
                    np.mean(fitness_avg, axis=0)[::every_nth] - np.std(fitness_avg, axis=0)[::every_nth],
                    np.mean(fitness_avg, axis=0)[::every_nth] + np.std(fitness_avg, axis=0)[::every_nth],
                    alpha=0.3, color='b')

    plt.plot(x_axis[::every_nth], np.mean(fitness_max, axis=0)[::every_nth], 'g-', label='Melhor Fitness')
    plt.fill_between(x_axis[::every_nth],
                    np.mean(fitness_max, axis=0)[::every_nth] - np.std(fitness_max, axis=0)[::every_nth],
                    np.mean(fitness_max, axis=0)[::every_nth] + np.std(fitness_max, axis=0)[::every_nth],
                    alpha=0.3, color='g')

    plt.plot(x_axis[::every_nth], np.mean(fitness_min, axis=0)[::every_nth], 'r-', label='Pior Fitness')
    plt.fill_between(x_axis[::every_nth],
                    np.mean(fitness_min, axis=0)[::every_nth] - np.std(fitness_min, axis=0)[::every_nth],
                    np.mean(fitness_min, axis=0)[::every_nth] + np.std(fitness_min, axis=0)[::every_nth],
                    alpha=0.3, color='r')
                    
    plt.ylabel('Fitness')
    plt.xlabel('Iteração')

    plt.ylim((ymin, ymax))

    plt.yticks(np.arange(0, ymax, args.yticks))

    plt.tight_layout()
    # plt.legend()

    head, tail = os.path.split(path)
    tail = tail[:-5]
    tail = tail.replace('.', '_')

    if not os.path.exists(os.path.join(head, 'imgs')):
        os.makedirs(os.path.join(head, 'imgs'))
    
    figs.append(os.path.join('imgs', tail+'.pdf'))
    plt.savefig(os.path.join(head, 'imgs', tail+'.pdf'))

save_table(figs, os.path.join(head, 'imgs'))