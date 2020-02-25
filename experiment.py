#!/usr/bin/env python2
import sys
import os
import subprocess
import time
from random import shuffle

"""
Type this to start:
    ./runner.py <algo filename> <n equals num> <number of iterations>

For example, typing:
    ./runner.py bfs.py 3 20

Translates to executing:
    python bfs.py
    on randomly generated 3x3 puzzles for 20 times
"""

# argv[0] represents the name of the file that is being executed
# argv[1] represents name of input file
# argv[2] represents size n of the puzzle
# argv[3] represents number of iterations to perform for the experiment
if len(sys.argv) != 4:
    print("Wrong number of arguments! Try:\n{0} <algo filename> <n equals num>.".format(sys.argv[0]))

filename = sys.argv[1]
puzzle_size = sys.argv[2]
number_of_iteratons = sys.argv[3]

output_file = "{size}x{size}_experiment.txt".format(size=puzzle_size)

# clean previous outputs
if os.path.isfile(output_file):
    subprocess.call(["rm", output_file])
subprocess.call(["touch", output_file])

# This functions generates a random puzzle of the specified dimension (side length).
def generate_random_puzzle(dimension):
    sequence = [i + 1 for i in range(dimension ** 2)]
    sequence[-1] = 0
    shuffle(sequence)
    
    # clean previous outputs:
    output_file = "experiment_input.txt"
    if os.path.isfile(output_file):
        subprocess.call(["rm", output_file])
    subprocess.call(["touch", output_file])

    # write into file:
    string_to_write = ""
    for i in range(dimension ** 2):
        if (i + 1)% dimension == 0:
            string_to_write += (str(sequence[i]) + "\n")
        else:
            string_to_write += (str(sequence[i]) + " ")
    experiment_input_file = open(output_file, "w")
    experiment_input_file.write(string_to_write)
    experiment_input_file.close()

# This function checks whether an output file contains UNSOLVABLE
def file_contains_unsolvable(file_name):
    text_file = open(file_name, "r")
    line = text_file.readline()
    text_file.close()
    return line == "UNSOLVABLE\n"

# array of all durations during the experiment
durations_for_solvable = []
durations_for_unsolvable = []

# randomly generates a puzzle
generate_random_puzzle(int(puzzle_size, base=10))
input_path = "experiment_input.txt"

# run program
for i in range(int(number_of_iteratons, base=10)):
    # start a timer
    start = time.time()
    #print("Running {filename} on {size}x{size} puzzle with random input".format(filename=filename, size=puzzle_size))
    subprocess.call(["python", filename, input_path, output_file])
    end = time.time()
    duration = round(end-start, 2)
    # check whether the puzzle is unsolvable
    if file_contains_unsolvable(output_file):
        durations_for_unsolvable.append(duration)
    else:
        durations_for_solvable.append(duration)
    #print("Completed.\nDuration: {0} seconds".format(duration))

    # prepare for next round
    # clean previous outputs
    if os.path.isfile(output_file):
        subprocess.call(["rm", output_file])
    subprocess.call(["touch", output_file])
    generate_random_puzzle(int(puzzle_size, base=10))

# print out all the durations at the end
print("SOLVABLE:")
for duration in durations_for_solvable:
    print(str(duration))
average_for_solvable = sum(durations_for_solvable) / len(durations_for_solvable)
print("average: " + str(average_for_solvable) + "s")

print("UNSOLVABLE:")
for duration in durations_for_unsolvable:
    print(str(duration))   
average_for_unsolvable = sum(durations_for_unsolvable) / len(durations_for_unsolvable)
print("average: " + str(average_for_unsolvable) + "s")     