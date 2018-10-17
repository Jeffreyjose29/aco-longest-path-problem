import os, json, argparse

import matplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt

import numpy as np

plt.style.use('ggplot')
f = plt.figure()
f.set_figheight(5)
f.set_figwidth(8)

with open('experiments/run1/sol_it1500_ant30_ipher0.1_evap0.1_alph1.15_bet1.0.json', 'r') as fhandle:
    score = json.loads(fhandle.read())

fitness_avg = []
fitness_max = []
fitness_min = []
for runs in score['Runs']:
    avg_iteration = []
    max_iteration = []
    min_iteration = []
    for key, iteration in runs.items():
        avg_iteration.append(np.mean(iteration['costs']))
        max_iteration.append(np.max(iteration['costs']))
        min_iteration.append(np.min(iteration['costs']))
    fitness_avg.append(avg_iteration)
    fitness_max.append(max_iteration)
    fitness_min.append(min_iteration)


x_axis = np.arange(0,len(fitness_avg[0]))

every_nth = 10

plt.plot(x_axis[::every_nth], np.mean(fitness_avg, axis=0)[::every_nth], 'b-')
plt.fill_between(x_axis[::every_nth],
                np.mean(fitness_avg, axis=0)[::every_nth] - np.std(fitness_avg, axis=0)[::every_nth],
                np.mean(fitness_avg, axis=0)[::every_nth] + np.std(fitness_avg, axis=0)[::every_nth],
                alpha=0.3, color='b')

plt.plot(x_axis[::every_nth], np.mean(fitness_max, axis=0)[::every_nth], 'g-')
plt.fill_between(x_axis[::every_nth],
                np.mean(fitness_max, axis=0)[::every_nth] - np.std(fitness_max, axis=0)[::every_nth],
                np.mean(fitness_max, axis=0)[::every_nth] + np.std(fitness_max, axis=0)[::every_nth],
                alpha=0.3, color='g')


plt.plot(x_axis[::every_nth], np.mean(fitness_min, axis=0)[::every_nth], 'r-')
plt.fill_between(x_axis[::every_nth],
                np.mean(fitness_min, axis=0)[::every_nth] - np.std(fitness_min, axis=0)[::every_nth],
                np.mean(fitness_min, axis=0)[::every_nth] + np.std(fitness_min, axis=0)[::every_nth],
                alpha=0.3, color='r')

plt.show()