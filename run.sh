#!/bin/bash

TIMESTAMP=$(date +%s)
SAVEDIR="TEST1"
RUNS=14
JOBS=7

echo "Graph 1"

############# NUMBER OF ANTS TEST
TEST="nb_ants"
echo "Running test $TEST"
declare -a arr_ants=("10" "20" "40" "80")
declare -a RUNS
for nb_ants in "${arr_ants[@]}"
do
    echo "$nb_ants ants"
    f1=$(python3 run.py --runs $RUNS --dataset graph1 --iterations 1000 --ants $nb_ants --evaporation 0.1 --alpha 1 --beta 1 --save-dir $SAVEDIR --sub-dir $TEST --jobs $JOBS | tail -1)
    RUNS=("${RUNS[@]}" "$f1")
done
python3 plots/plot_fitness.py --paths "${RUNS[@]}"

############# EVAPORATION TEST
TEST="evaporation"
echo "Running test $TEST"
declare -a arr_ants=("0.01" "0.05" "0.1" "0.2")
declare -a RUNS
for evap in "${arr_ants[@]}"
do
    echo "$evap ants"
    f1=$(python3 run.py --runs $RUNS --dataset graph1 --iterations 1000 --ants 40 --evaporation $evap --alpha 1.1 --beta 1 --save-dir $SAVEDIR --sub-dir $TEST --jobs $JOBS | tail -1)
    RUNS=("${RUNS[@]}" "$f1")
done
python3 plots/plot_fitness.py --paths "${RUNS[@]}"

############# ALPHA TEST
TEST="alpha"
echo "Running test $TEST"
declare -a arr_ants=("1" "1.1" "1.2" "1.3")
declare -a RUNS
for alpha in "${arr_ants[@]}"
do
    echo "Alpha = $alpha"
    f1=$(python3 run.py --runs $RUNS --dataset graph1 --iterations 1000 --ants 40 --evaporation 0.1 --alpha $alpha --beta 1 --save-dir $SAVEDIR --sub-dir $TEST --jobs $JOBS | tail -1)
    RUNS=("${RUNS[@]}" "$f1")
done
python3 plots/plot_fitness.py --paths "${RUNS[@]}"

############# BETA TEST
TEST="beta"
echo "Running test $TEST"
declare -a arr_ants=("1" "1.1" "1.2" "1.3")
declare -a RUNS
for beta in "${arr_ants[@]}"
do
    echo "Beta = $beta"
    f1=$(python3 run.py --runs $RUNS --dataset graph1 --iterations 1000 --ants 40 --evaporation 0.1 --alpha 1.1 --beta $beta --save-dir $SAVEDIR --sub-dir $TEST --jobs $JOBS | tail -1)
    RUNS=("${RUNS[@]}" "$f1")
done
python3 plots/plot_fitness.py --paths "${RUNS[@]}"