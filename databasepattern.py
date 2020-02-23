import sys
import time
from collections import deque

actions = ["DOWN", "UP", "RIGHT", "LEFT"]

def create_initial_state(dimension, sample):
    sequence = [0 for i in range(dimension ** 2)]
    for i in range(len(sample)):
        initial_position = sample[i]
        sequence[initial_position - 1] = initial_position
    return tuple(sequence)

# This move function behaves differently from the move function in our BFS/A* search.
# It moves the tile at the given position according to the direction given.
def move(dimension, state, direction, position):
        new_state = list(state)
        if direction == "DOWN" and position < (len(state) - dimension) and new_state[position + dimension] == 0:
            # This moves the tile at the given position down to a blank tile
            new_state[position], new_state[position + dimension] = new_state[position + dimension], new_state[position]

        elif direction == "UP" and position > (dimension - 1) and new_state[position - dimension] == 0:
            # This moves the tile at the given position up to a blank tile
            new_state[position], new_state[position - dimension] = new_state[position - dimension], new_state[position]

        elif direction == "RIGHT" and (position % dimension) != (dimension - 1) and new_state[position + 1] == 0:
            # This moves the tile at the given position right to a blank tile
            new_state[position], new_state[position + 1] = new_state[position + 1], new_state[position]

        elif direction == "LEFT" and (position % dimension) != 0 and new_state[position - 1] == 0:
            # This moves the tile at the given position left to a blank tile
            new_state[position], new_state[position - 1] = new_state[position - 1], new_state[position]
        else:
            return None
        return tuple(new_state)

def bfs(initial_state, dimension, subset):
    dictionary = {initial_state: 0}
    frontier = deque([initial_state])

    while len(frontier) > 0:
        current_state = frontier.popleft()
        for i in subset:
            position = current_state.index(i)

            for action in actions:
                new_state = move(dimension, current_state, action, position)
                if new_state != None and new_state not in dictionary:
                    dictionary[new_state] = dictionary[current_state] + 1
                    frontier.append(new_state)
    
    return dictionary

def print_in_grid(dimension, state):
    for i in range(dimension):
        row = []
        for j in range(dimension):
            row.append(state[i * dimension + j])
        print(row)

if __name__ == "__main__":

    try:
        if len(sys.argv) < 4:
            raise ValueError("Wrong number of arguments! Try:\n{0} <output file> <grid dimension> <size of subproblem> <subproblem inputs...>." \
                .format(sys.argv[0]))
    except ValueError as error:
            sys.exit(error)
    
    grid_dimension = int(sys.argv[2], base = 10)
    subset_size = int(sys.argv[3], base = 10)

    try:
        if len(sys.argv[4:]) != subset_size:
            raise ValueError("Number of subproblem inputs, {actual_num}, is not equal to size of the subproblem, {expected_num}." \
                    .format(actual_num = len(sys.argv[3:]), expected_num = subset_size))
    except ValueError as error:
        sys.exit(error)

    subset = []
    for i in sys.argv[4:]:
        subset.append( int(i, base = 10))

    print("Subset selected:", subset)

    initial_state = create_initial_state(grid_dimension, subset)
    print("Initial state:")
    print_in_grid(grid_dimension, initial_state)

    start = time.time()
    dictionary = bfs(initial_state, grid_dimension, subset)
    end = time.time()

    dictionary_values = dictionary.values()
    num_of_states = len(dictionary_values)
    max_steps = max(dictionary_values)
    avg_steps = sum(dictionary_values) / num_of_states
    time_taken = round(end - start, 2)

    print("Statistics:")
    print("Number of states found:", num_of_states)
    print("Largest number of steps:", max_steps)
    print("Average number of steps:", avg_steps)
    print("Time taken: {0} seconds".format(time_taken))


    with open(sys.argv[1], 'a') as f:
        f.write("Subset selected: ")
        f.write(str(subset) + "\n")
        f.write("Initial state: ")
        f.write(str(initial_state) + "\n")
        f.write("Number of states found: ")
        f.write(str(num_of_states) + "\n")
        f.write("Largest number of steps: ")
        f.write(str(max_steps) + "\n")
        f.write("Average number of steps: ")
        f.write(str(avg_steps) + "\n")
        f.write("Time taken: ")
        f.write(str(time_taken) + " seconds\n")
        
        for i in dictionary:
            f.write(str(i) + ": ")
            f.write(str(dictionary[i]) + "\n")





    





