#!/usr/bin/env python2
import sys
import os
import subprocess
import time
from random import shuffle
from random import randrange
from CS3243_P1_33_1 import Puzzle as BfsPuzzle
from CS3243_P1_33_2 import Puzzle as EuclideanPuzzle
from CS3243_P1_33_3 import Puzzle as RelaxedAdjacencyPuzzle
from CS3243_P1_33_4 import Puzzle as LinearConflictPuzzle

"""
To run the experiments, run ./CS3243_P1_33_5.py in the terminal.
The experiments consist of two parts, starting from Line 167.
At the end of the experiments, two CSV files containing the
experimental results, experiment_1_output.csv and experiment_2_output.csv,
will be generated.
"""

################### TESTCASES ######################

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

# 5x5 test case 4
initial_state_5_4 = [[1,3,4,10,5],
                     [7,2,12,8,14],
                     [6,11,13,15,0],
                     [17,23,18,9,19],
                     [16,21,22,24,20]]

# 5x5 test case 4
initial_state_5_5 = [[1,2,3,4,5],
                     [6,7,8,9,10],
                     [11,12,14,0,15],
                     [16,17,13,18,19],
                     [21,22,23,24,20]]

###################### UTILITY FUNCTIONS ######################
# This function returns an array of [number_of_nodes_expanded, size_of_frontier, number_of_steps, time_taken]
def run_and_generate_stats(puzzle):
    start = time.time()
    ans = puzzle.solve()
    end = time.time()
    duration = round(end - start, 3)
    stats = puzzle.get_statistics()
    stats.append(duration)
    return stats

# This function is used to check for solvability of puzzles
def grid_parity(state, size):
    state_list = list(state)
    state_list.remove(0)
    has_visited = [False] * len(state_list) # Helps to keep track which number has been visited
    num_of_cycles = 0
    for num in state_list:
        if not has_visited[num - 1]:
            # If the number at the index has not been visited yet, we
            # will begin exploring it to identify the cycle it is part of.
            has_visited[num - 1] = True 
            num_of_cycles += 1
            next_in_cycle = num
            while state_list[next_in_cycle - 1] != num:
                # We continue visiting all the numbers in the cycle until
                # we reach the starting point.
                next_in_cycle = state_list[next_in_cycle - 1]
                has_visited[next_in_cycle - 1] = True

    if size % 2 == 1:
        # For odd size, invariant is the parity of the number of transpositions
        return (len(state_list) - num_of_cycles) % 2
    else:
        # For even size, invariant is the parity of number of transpositions + vertical distance of blank tile
        return (len(state_list) - num_of_cycles + (state.index(0) // size) ) % 2

def test_algos_for_size_n(algos, testcases, goalstate):
    """
    This function runs all the algorithms in 'algos' on all the testcases in
    'testcases', and stores the results in 'result'.

    algos: list of puzzle classes to instantiate
    testcases: list of unsolved puzzle states, all of size n.
    goalstate: 2D list representing the goal state of a size n puzzle
    """
    
    results = []

    for testcase in testcases:
        for algo in algos:
            puzzle = algo(testcase, goalstate)
            result = run_and_generate_stats(puzzle)
            results.append(result)
    
    return results
    

################################################################################
#################### Experiment 1: Clear all test cases ########################
################################################################################
"""
In this section, we run all the test cases as proof of concept that our
algorithms work as expected (BFS is only tested for 3x3 puzzles). Note that the 
results for unsolvable cases will be 0.
"""

print("\n===============================")
print("BEGINNING EXPERIMENT 1:")
print("===============================\n")

inputs_for_3x3 = [initial_state_3_1, initial_state_3_2, initial_state_3_3]
inputs_for_4x4 = [initial_state_4_1, initial_state_4_2, initial_state_4_3]
inputs_for_5x5 = [initial_state_5_1, initial_state_5_2, initial_state_5_3, initial_state_5_4, initial_state_5_5]

# Run BFS, Euclidean, Max(Relaxed Adjacency, Manhattan), Linear Conflict on 3x3 puzzle
print("Running 3x3 public testcases...")
algos_3x3 = [BfsPuzzle, EuclideanPuzzle, RelaxedAdjacencyPuzzle, LinearConflictPuzzle]
results_3x3 = test_algos_for_size_n(algos_3x3, inputs_for_3x3, goal_state_3)
print("3x3 clear")

# Run Euclidean, Max(Relaxed Adjacency, Manhattan), Linear Conflict on 4x4 puzzle
print("Running 4x4 public testcases...")
algos_4x4 = [EuclideanPuzzle, RelaxedAdjacencyPuzzle, LinearConflictPuzzle]
results_4x4 = test_algos_for_size_n(algos_4x4, inputs_for_4x4, goal_state_4)
print("4x4 clear")

# Run Euclidean, Max(Relaxed Adjacency, Manhattan), Linear Conflict on 4x4 puzzle
print("Running 5x5 public testcases...")
algos_5x5 = [EuclideanPuzzle, RelaxedAdjacencyPuzzle, LinearConflictPuzzle]
results_5x5 = test_algos_for_size_n(algos_5x5, inputs_for_5x5, goal_state_5)
print("5x5 clear")

###### Write into a CSV file ######
output_file = "experiment_1_output.csv"

# clean previous outputs
if os.path.isfile(output_file):
    os.remove(output_file)

delimiter = ","
algorithm_names_for_3x3 = ["BFS", "Euclidean", "\"Max(Relaxed Adjacency, Manhattan)\"", "Linear Conflict"]
algorithm_names_for_larger = ["Euclidean", "\"Max(Relaxed Adjacency, Manhattan)\"", "Linear Conflict"]
table_headings = "Algorithm,Nodes expanded,Size of frontier,Number of steps,Time taken\n"
with open(output_file, 'w+') as f:
    # 3x3
    num_algos = len(algos_3x3)
    f.write("For 3x3 inputs\n")
    f.write(table_headings)
    for count, result in enumerate(results_3x3):
        if (count % num_algos) == 0:
            f.write("Input {}\n".format(count // num_algos + 1))
        algorithm_name = algorithm_names_for_3x3[count % len(algorithm_names_for_3x3)]   
        f.write(algorithm_name + delimiter + delimiter.join(str(x) for x in result) +'\n')

    # 4x4
    num_algos = len(algos_4x4)
    f.write("For 4x4 inputs\n")
    f.write(table_headings)
    for count, result in enumerate(results_4x4):
        if (count % num_algos) == 0:
            f.write("Input {}\n".format(count // num_algos + 1))
        algorithm_name = algorithm_names_for_larger[count % len(algorithm_names_for_larger)]
        f.write(algorithm_name + delimiter + delimiter.join(str(x) for x in result) +'\n')

    # 5x5
    num_algos = len(algos_5x5)
    f.write("For 5x5 inputs\n")
    f.write(table_headings)
    for count, result in enumerate(results_5x5):
        if (count % num_algos) == 0:
            f.write("Input {}\n".format(count // num_algos + 1))
        algorithm_name = algorithm_names_for_larger[count % len(algorithm_names_for_larger)]    
        f.write(algorithm_name + delimiter + delimiter.join(str(x) for x in result) +'\n')

print("Experiment 1 completed.\n")


################################################################################
#################### Experiment 2: Comparing heuristics ########################
################################################################################
"""
In this section, we test and compare the efficacies of the different heuristics.
This is done by randomly generating puzzles of solution lengths 1 to N, and then
comparing the metrics of each alogrithm for the puzzles generated. This
information will then be used to plot a graph of solution length against the
matric measured, allowing us to objectively comapare each solution's pros and
cons.

Since 3x3 puzzles are too trivial for the heuristics, we only generated puzzles
of dimensions 4x4 and 5x5
"""

def generate_puzzles(number, size, step):

    # This function helps to generate a new state by moving a tile in a particular direction into the blank tile.
    # state: the current state of the grid
    # dir: the direction in which a tile will move into the blank tile
    # pos: the position of the blank tile
    def move(state, dir, pos):
        new_state = list(state)
        if dir == "DOWN" and pos > (size - 1):
            # A tile can only move down into the blank tile if the blank tile is not in the first row.
            new_state[pos], new_state[pos - size] = new_state[pos - size], new_state[pos]

        elif dir == "UP" and pos < (len(state) - size):
            # A tile can only move up into the blank tile if the blank tile is not in the last row.
            new_state[pos], new_state[pos + size] = new_state[pos + size], new_state[pos]

        elif dir == "RIGHT" and (pos % size) != 0:
            # A tile can only move right into the blank tile if the blank tile is not to the utmost left.
            new_state[pos], new_state[pos - 1] = new_state[pos - 1], new_state[pos]

        elif dir == "LEFT" and (pos % size) != (size - 1):
            # A tile can only move left into the blank tile if the blank tile is not to the utmost right.
            new_state[pos], new_state[pos + 1] = new_state[pos + 1], new_state[pos]
        else:
            return None
        return tuple(new_state)

    def dfs(state, visited, solution_length, actions):
        if solution_length == 0:
            return state
        pos = state.index(0)
        visited.add(state)
        shuffle(actions)
        for a in actions:
            new_state = move(state, a, pos)
            if new_state not in visited and new_state != None:
                state = dfs(new_state, visited, solution_length-1, actions)
                return state

    
    actions = ["DOWN", "UP", "RIGHT", "LEFT"]
    start = [i for i in range(1, size ** 2 + 1)]
    start[-1] = 0
    start_state = tuple(start)
    goalstate = [[j*size+i for i in range(1, size+1)] for j in range(size)]
    goalstate[-1][-1] = 0

    puzzles = []
    count = [i for i in range(1, number + 1, step)]
    while len(count) > 0:
        visited = set([start_state])
        puzzle = dfs(start_state, visited, max(count), actions)
        if puzzle is None:
            continue
        # convert to 2D list
        puzzle = [[puzzle[i*size+j] for j in range(size)] for i in range(size)]

        solver = RelaxedAdjacencyPuzzle(puzzle, goalstate)
        ans = solver.solve()
        if len(ans) in count:
            count.remove(len(ans))
            puzzles.append(puzzle)
    
    return puzzles

print("===============================")
print("BEGINNING EXPERIMENT 2:")
print("===============================\n")

# Generate puzzles
N = 35
step_size = 1

puzzles_4x4 = generate_puzzles(N, 4, step_size)
print("Generated random 4x4 puzzles")

puzzles_5x5 = generate_puzzles(N, 5, step_size)
print("Generated random 5x5 puzzles")

# Run Euclidean, Max(Relaxed Adjacency, Manhattan), Linear Conflict on 4x4 puzzle
print("Running 4x4 puzzles...")
euclidean_results_4x4 = test_algos_for_size_n([EuclideanPuzzle], puzzles_4x4, goal_state_4)
relaxed_adjacency_results_4x4 = test_algos_for_size_n([RelaxedAdjacencyPuzzle], puzzles_4x4, goal_state_4)
lconflict_results_4x4 = test_algos_for_size_n([LinearConflictPuzzle], puzzles_4x4, goal_state_4)
print("4x4 clear")

# Run Euclidean, Max(Relaxed Adjacency, Manhattan), Linear Conflict on 4x4 puzzle
print("Running 5x5 puzzles...")
euclidean_results_5x5 = test_algos_for_size_n([EuclideanPuzzle], puzzles_5x5, goal_state_5)
relaxed_adjacency_results_5x5 = test_algos_for_size_n([RelaxedAdjacencyPuzzle], puzzles_5x5, goal_state_5)
lconflict_results_5x5 = test_algos_for_size_n([LinearConflictPuzzle], puzzles_5x5, goal_state_5)
print("5x5 clear")


###### Write into a CSV file ######
output_file = "experiment_2_output.csv"

# clean previous outputs
if os.path.isfile(output_file):
    os.remove(output_file)

delimiter = ","
with open(output_file, 'w+') as f:
    # 4x4
    f.write("For 4x4 inputs\n")
    f.write("Nodes expanded,Size of frontier,Number of steps,Time taken\n")

    results_4x4 = [euclidean_results_4x4, relaxed_adjacency_results_4x4, lconflict_results_4x4]
    names = ["Euclidean", "Max(Relaxed Adjacency, Manhattan)", "Linear Conflict"]
    for i, algo_results in enumerate(results_4x4):
        f.write(names[i] + '\n')
        for result in algo_results:
            f.write(delimiter.join(str(x) for x in result) +'\n')

    # 5x5
    f.write("For 5x5 inputs\n")
    f.write("Nodes expanded,Size of frontier,Number of steps,Time taken\n")

    results_5x5 = [euclidean_results_5x5, relaxed_adjacency_results_5x5, lconflict_results_5x5]
    names = ["Euclidean", "Max(Relaxed Adjacency, Manhattan)", "Linear Conflict"]
    for i, algo_results in enumerate(results_5x5):
        f.write(names[i] + '\n')
        for result in algo_results:
            f.write(delimiter.join(str(x) for x in result) +'\n')

print("Experiment 2 completed.")
