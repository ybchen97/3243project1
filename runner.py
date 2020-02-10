#!/usr/bin/env python2

import sys
import os
import subprocess
import time

"""
HOW IT WORKS:
    ./runner.py <algo filename> <n equals num> <test input num>

For example, typing:
    ./runner.py bfs.py 3 1

Translates to executing:
    python bfs.py public_tests_p1/n_equals_3/input_1.txt 3x3_input_1.out
"""

# argv[0] represents the name of the file that is being executed
# argv[1] represents name of input file
# argv[2] represents size n of the puzzle
# argv[3] represents input number of test case
if len(sys.argv) != 4:
    print("Wrong number of arguments! Try:\n{0} <algo filename> <n equals num> <test input num>.".format(sys.argv[0]))

filename = sys.argv[1]
puzzle_size = sys.argv[2]
input_num = sys.argv[3]

input_path = "public_tests_p1/n_equals_{size}/input_{n}.txt".format(size=puzzle_size, n=input_num)
output_file = "{size}x{size}_input_{n}.out".format(size=puzzle_size, n=input_num)

# clean previous outputs
if os.path.isfile(output_file):
    subprocess.call(["rm", output_file])
subprocess.call(["touch", output_file])

# start a timer
start = time.time()

# run program
print("Running {filename} on {size}x{size} puzzle with input_{n}.txt".format(filename=filename, size=puzzle_size, n=input_num))
subprocess.call(["python", filename, input_path, output_file])
end = time.time()
print("Completed.\nDuration: {0} seconds".format(round(end-start, 2)))

# option to run solver to check for correctness
if (input_num != "1"):
    cat = subprocess.Popen(('cat', output_file), stdout=subprocess.PIPE)
    length = subprocess.check_output(('wc', '-l'), stdin=cat.stdout)
    cat.wait()
    print("Solution length: " + str(length).strip())
    run_solver = raw_input("Run solver.py? (y/n)\n")
    if (run_solver == "y"):
        subprocess.call(["python", "solver.py", input_path, output_file])

