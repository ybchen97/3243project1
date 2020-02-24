#!/usr/bin/env python2
import sys
import os
import subprocess
import time
from random import shuffle
from bfs import Puzzle as BfsPuzzle
from manhattan import Puzzle as ManhattanPuzzle
from linearconflict import Puzzle as LinearConflictPuzzle
from subproblem import Puzzle as SubproblemPuzzle

output_file = "experiment_output.csv"

# clean previous outputs
if os.path.isfile(output_file):
    subprocess.call(["rm", output_file])
subprocess.call(["touch", output_file])

# This functions generates a random puzzle of the specified dimension (side length).
def generate_random_puzzle(dimension):
    sequence = [i + 1 for i in range(dimension ** 2)]
    sequence[-1] = 0
    shuffle(sequence)

    # convert to 2D list
    puzzle = [[0 for i in range(n)] for j in range(n)]
    counter = 0
    for i in range(dimension):
        for j in range(dimension):
            puzzle[i][j] = sequence[counter]
            counter += 1

    return puzzle

# This function returns an array of [number_of_nodes_expanded, size_of_frontier, number_of_steps, time_taken]
def run_and_generate_stats(puzzle):
    start = time.time()
    ans = puzzle.solve()
    end = time.time()
    duration = round(end - start, 2)
    stats = puzzle.get_statistics()
    stats.append(duration)
    return stats

################### Experiment 1.1: 3x3 PUZZLES ######################
# Note that the results for unsolvable cases will be 0.
results_3x3 = []
results_4x4 = []
results_5x5 = []

# 3x3
n = 3
max_num = n ** 2 - 1
goal_state_3 = [[0 for i in range(n)] for j in range(n)]
for i in range(1, max_num + 1):
    goal_state_3[(i-1)//n][(i-1)%n] = i
goal_state_3[n - 1][n - 1] = 0

# 3x3 test case 1
initial_state_3_1 = [[1,2,3],
                     [4,5,6],
                     [8,7,0]]
# 3x3 test case 2
initial_state_3_2 = [[1,8,3],
                     [5,2,4],
                     [0,7,6]]
# 3x3 test case 3
initial_state_3_3 = [[8,6,7],
                     [2,5,4],
                     [3,0,1]]
inputs_for_3x3 = [initial_state_3_1, initial_state_3_2, initial_state_3_3]

for initial_state in inputs_for_3x3:
    ##### BFS #####
    bfs_puzzle = BfsPuzzle(initial_state, goal_state_3)
    result = run_and_generate_stats(bfs_puzzle)
    results_3x3.append(result)

    ##### A* Manhattan #####
    manhattan_puzzle = ManhattanPuzzle(initial_state, goal_state_3)
    result = run_and_generate_stats(manhattan_puzzle)
    results_3x3.append(result)

    ##### A* Linear Conflict #####
    linear_conflict_puzzle = LinearConflictPuzzle(initial_state, goal_state_3)
    result = run_and_generate_stats(linear_conflict_puzzle)
    results_3x3.append(result)

    ##### A* Subproblem #####
    subproblem_puzzle = SubproblemPuzzle(initial_state, goal_state_3)
    result = run_and_generate_stats(subproblem_puzzle)
    results_3x3.append(result)

# 4x4
n = 4
max_num = n ** 2 - 1
goal_state_4 = [[0 for i in range(n)] for j in range(n)]
for i in range(1, max_num + 1):
    goal_state_4[(i-1)//n][(i-1)%n] = i
goal_state_4[n - 1][n - 1] = 0

# 4x4 test case 1
initial_state_4_1 = [[1,2,3,4],
                     [5,6,7,8],
                     [10,11,0,12],
                     [9,13,15,14]]
# 4x4 test case 2
initial_state_4_2 = [[12,15,6,10],
                     [4,9,5,8],
                     [14,13,0,2],
                     [1,7,11,3]]
# 4x4 test case 3
initial_state_4_3 = [[13,5,3,4],
                     [2,1,8,0],
                     [9,15,10,11],
                     [14,12,6,7]]
inputs_for_4x4 = [initial_state_4_1, initial_state_4_2, initial_state_4_3]

for initial_state in inputs_for_4x4:
    ##### BFS #####
    # bfs_puzzle = BfsPuzzle(initial_state, goal_state_4)
    # result = run_and_generate_stats(bfs_puzzle)
    # results_4x4.append(result)

    ##### A* Manhattan #####
    manhattan_puzzle = ManhattanPuzzle(initial_state, goal_state_4)
    result = run_and_generate_stats(manhattan_puzzle)
    results_4x4.append(result)

    ##### A* Linear Conflict #####
    linear_conflict_puzzle = LinearConflictPuzzle(initial_state, goal_state_4)
    result = run_and_generate_stats(linear_conflict_puzzle)
    results_4x4.append(result)

    # ##### A* Subproblem #####
    # subproblem_puzzle = SubproblemPuzzle(initial_state, goal_state_4)
    # result = run_and_generate_stats(subproblem_puzzle)
    # results_4x4.append(result)

# 5x5
n = 5
max_num = n ** 2 - 1
goal_state_5 = [[0 for i in range(n)] for j in range(n)]
for i in range(1, max_num + 1):
    goal_state_5[(i-1)//n][(i-1)%n] = i
goal_state_5[n - 1][n - 1] = 0

# 5x5 test case 1
initial_state_5_1 = [[1,2,3,4,5],
                     [6,7,8,9,10],
                     [11,12,0,14,15],
                     [16,17,13,20,19],
                     [21,22,23,18,24]]
# 5x5 test case 2
initial_state_5_2 = [[1,3,4,10,5],
                     [7,2,8,0,14],
                     [6,11,12,9,15],
                     [16,17,13,18,19],
                     [21,22,23,24,20]]
# 5x5 test case 3
initial_state_5_3 = [[1,3,4,0,10],
                     [7,2,12,8,5],
                     [6,11,13,15,14],
                     [17,23,18,9,19],
                     [16,21,22,24,20]]
inputs_for_5x5 = [initial_state_5_1, initial_state_5_2, initial_state_5_3]

for initial_state in inputs_for_5x5:
    ##### BFS #####
    # bfs_puzzle = BfsPuzzle(initial_state, goal_state_5)
    # result = run_and_generate_stats(bfs_puzzle)
    # results_5x5.append(result)

    ##### A* Manhattan #####
    manhattan_puzzle = ManhattanPuzzle(initial_state, goal_state_5)
    result = run_and_generate_stats(manhattan_puzzle)
    results_5x5.append(result)

    ##### A* Linear Conflict #####
    linear_conflict_puzzle = LinearConflictPuzzle(initial_state, goal_state_5)
    result = run_and_generate_stats(linear_conflict_puzzle)
    results_5x5.append(result)

    # ##### A* Subproblem #####
    # subproblem_puzzle = SubproblemPuzzle(initial_state, goal_state_5)
    # result = run_and_generate_stats(subproblem_puzzle)
    # results_5x5.append(result)

###### Write into a CSV file ######
delimiter = ","
with open(output_file, 'a') as f:
    # 3x3
    f.write("For 3x3 inputs\n")
    f.write("Nodes expanded,Size of frontier,Number of steps,Time taken\n")
    for result in results_3x3:
        f.write(delimiter.join(str(x) for x in result) +'\n')

    # 4x4
    f.write("For 4x4 inputs\n")
    f.write("Nodes expanded,Size of frontier,Number of steps,Time taken\n")
    for result in results_4x4:
        f.write(delimiter.join(str(x) for x in result) +'\n')

    # 5x5
    f.write("For 5x5 inputs\n")
    f.write("Nodes expanded,Size of frontier,Number of steps,Time taken\n")
    for result in results_5x5:
        f.write(delimiter.join(str(x) for x in result) +'\n')
   