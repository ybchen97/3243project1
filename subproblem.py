import sys
import random
import heapq
import time
from collections import deque

class Puzzle(object):
    def __init__(self, init_state, goal_state):
        # you may add more attributes if you think is useful
        self.size = len(init_state) # size refers to the self.size of the grid
        self.init_state = self.flatten(init_state)
        self.goal_state = self.flatten(goal_state)
        self.actions = ["DOWN", "UP", "RIGHT", "LEFT"]

        self.subset_one = ""
        self.subset_two = ""
        if self.size == 3:
            self.subset_one = [1, 2, 3, 4]
            self.subset_two = [5, 6, 7, 8]
        else:            
            #get upper triangle subset
            self.subset_one = [i for row in goal_state[:-1] for i in row[goal_state.index(row) + 1:]]
            #get lower triangle subset
            self.subset_two = [i for row in goal_state[1:] for i in row[:goal_state.index(row)]]
        print(self.subset_one)
        start = time.time()
        initial_state_one = self.create_initial_state(self.subset_one)
        self.dictionary_one = self.bfs(initial_state_one, self.subset_one)

        print(self.subset_two)
        mid = time.time()
        initial_state_two = self.create_initial_state(self.subset_two)
        self.dictionary_two = self.bfs(initial_state_two, self.subset_two)
        end = time.time()
        print("Sub 1: {:.2f}\nSub 2: {:.2f}\nTotal: {:.2f}\n".format(mid-start,end-mid,end-start))
        

    def solve(self):
        if self.grid_parity(self.init_state) != self.grid_parity(self.goal_state):
            return ['UNSOLVABLE']

        initial_evaluation = self.calculate_evaluation_function(self.init_state, 0)

        # Frontier nodes stored as a tuple:
        # node[0] = value of f(n)
        # node[1] = current state
        # node[2] = value of g(n), actual cost to get from initial state to current state
        frontier = [(initial_evaluation, self.init_state, 0)] 

        # Visited stores a key-value pair, with the key being the state of the grid and value being the current lowest 
        # value calculated by the evaluation function
        visited = {self.init_state: initial_evaluation}
        parent = {self.init_state: (None, None)} #(prev_state, direction)

        while len(frontier) > 0:
            # Removes the current node
            current_node = heapq.heappop(frontier)
            current_state = current_node[1]

            # For A* search, can only check for goal state when node is selected for expansion.
            # Otherwise, the output path may not optimal.
            if current_state == self.goal_state:
                break

            # Checks if the current node has the updated lower evaluation value
            if (current_state in visited and visited[current_state] == current_node[0]) :
                position = self.get_zero(current_state)

                for a in self.actions:
                    new_state = self.move(current_state, a, position)
                    if new_state != None:
                        actual_cost = current_node[2] + 1 # Updates the actual cost required to get to current node
                        evaluation_cost = self.calculate_evaluation_function(new_state, actual_cost)
                        if (new_state in visited and evaluation_cost < visited[new_state]) or (new_state not in visited):
                            # Node is only added into the frontier if the new evaluation cost is lower or has not been visited
                            parent[new_state] = (current_state, a)
                            visited[new_state] = evaluation_cost
                            heapq.heappush(frontier, (evaluation_cost, new_state, actual_cost))

        final_answer = []
        backtrack_state = self.goal_state
        while backtrack_state in parent and backtrack_state != self.init_state:
            final_answer.insert(0, parent[backtrack_state][1])
            backtrack_state = parent[backtrack_state][0]

        print("Length of visited: {0}".format(len(visited)))
        return final_answer

    # you may add more functions if you think is useful

    # This function helps to convert the grid representation to a tuple representation
    def flatten(self, grid):
        flattened_grid = [0] * (self.size ** 2)
        i = 0
        for j in range(self.size):
            for k in range(self.size):
                flattened_grid[i] = grid[j][k]
                i += 1
        return tuple(flattened_grid)

    def get_zero(self, state):
        return state.index(0)

    def grid_parity(self, state):
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

        if self.size % 2 == 1:
            # For odd size, invariant is the parity of the number of transpositions
            return (len(state_list) - num_of_cycles) % 2
        else:
            # For even size, invariant is the parity of number of transpositions + vertical distance of blank tile
           return (len(state_list) - num_of_cycles + (self.get_zero(state) // self.size) ) % 2

    # This function helps to generate a new state by moving a tile in a particular direction into the blank tile.
    # state: the current state of the grid
    # dir: the direction in which a tile will move into the blank tile
    # pos: the position of the blank tile
    def move(self, state, dir, pos):
        new_state = list(state)
        if dir == "DOWN" and pos > (self.size - 1):
            # A tile can only move down into the blank tile if the blank tile is not in the first row.
            new_state[pos], new_state[pos - self.size] = new_state[pos - self.size], new_state[pos]

        elif dir == "UP" and pos < (len(state) - self.size):
            # A tile can only move up into the blank tile if the blank tile is not in the last row.
            new_state[pos], new_state[pos + self.size] = new_state[pos + self.size], new_state[pos]

        elif dir == "RIGHT" and (pos % self.size) != 0:
            # A tile can only move right into the blank tile if the blank tile is not to the utmost left.
            new_state[pos], new_state[pos - 1] = new_state[pos - 1], new_state[pos]

        elif dir == "LEFT" and (pos % self.size) != (self.size - 1):
            # A tile can only move left into the blank tile if the blank tile is not to the utmost right.
            new_state[pos], new_state[pos + 1] = new_state[pos + 1], new_state[pos]
        else:
            return None
        return tuple(new_state)

    # This move function behaves differently from the move function in our BFS/A* search.
    # It moves the tile at the given position according to the direction given.
    def subproblem_move(self, state, direction, position):
        new_state = list(state)
        if direction == "DOWN" and position < (len(state) - self.size) and new_state[position + self.size] == 0:
            # This moves the tile at the given position down to a blank tile
            new_state[position], new_state[position + self.size] = new_state[position + self.size], new_state[position]

        elif direction == "UP" and position > (self.size - 1) and new_state[position - self.size] == 0:
            # This moves the tile at the given position up to a blank tile
            new_state[position], new_state[position - self.size] = new_state[position - self.size], new_state[position]

        elif direction == "RIGHT" and (position % self.size) != (self.size - 1) and new_state[position + 1] == 0:
            # This moves the tile at the given position right to a blank tile
            new_state[position], new_state[position + 1] = new_state[position + 1], new_state[position]

        elif direction == "LEFT" and (position % self.size) != 0 and new_state[position - 1] == 0:
            # This moves the tile at the given position left to a blank tile
            new_state[position], new_state[position - 1] = new_state[position - 1], new_state[position]
        else:
            return None
        return tuple(new_state)

    # This BFS function is used to find the solutions of the given subproblem
    def bfs(self, initial_state, subset):
        dictionary = {initial_state: 0}
        frontier = deque([initial_state])

        while len(frontier) > 0:
            current_state = frontier.popleft()
            for i in subset:
                position = current_state.index(i)

                for action in self.actions:
                    new_state = self.subproblem_move(current_state, action, position)
                    if new_state != None and new_state not in dictionary:
                        dictionary[new_state] = dictionary[current_state] + 1
                        frontier.append(new_state)
    
        return dictionary

    # This function helps to create the initial state based on our given subset of numbers
    def create_initial_state(self, subset):
        sequence = [0 for i in range(self.size ** 2)]
        for i in range(len(subset)):
            initial_position = subset[i]
            sequence[initial_position - 1] = initial_position
        return tuple(sequence)

    # This function helps to extract the pattern of the subset in the current state.
    # Example: if current state = (1, 2, 3, 4, 5, 6, 7, 8, 0) and subset = [1, 2, 3, 4], 
    #          then this function should return (1, 2, 3, 4, 0, 0, 0, 0, 0).
    def extract_subpattern(self, state, subset):
        subpattern = [0] * (self.size ** 2)
        for i in range(self.size ** 2):
            if state[i] in subset:
                subpattern[i] = state[i]
        return tuple(subpattern)

    def calculate_evaluation_function(self, state, current_cost):
        subpattern_one = self.extract_subpattern(state, set(self.subset_one))
        subpattern_two = self.extract_subpattern(state, set(self.subset_two))
        result = current_cost
        if subpattern_one in self.dictionary_one:
            result += self.dictionary_one[subpattern_one]
        if subpattern_two in self.dictionary_two:
            result += self.dictionary_two[subpattern_two]
        return result

if __name__ == "__main__":
    # do NOT modify below

    # argv[0] represents the name of the file that is being executed
    # argv[1] represents name of input file
    # argv[2] represents name of destination output file
    if len(sys.argv) != 3:
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        raise IOError("Input file not found!")

    lines = f.readlines()
    
    # n = num rows in input file
    n = len(lines)
    # max_num = n to the power of 2 - 1
    max_num = n ** 2 - 1

    # Instantiate a 2D list of size n x n
    init_state = [[0 for i in range(n)] for j in range(n)]
    goal_state = [[0 for i in range(n)] for j in range(n)]
    

    i,j = 0, 0
    for line in lines:
        for number in line.split(" "):
            if number == '':
                continue
            value = int(number , base = 10)
            if  0 <= value <= max_num:
                init_state[i][j] = value
                j += 1
                if j == n:
                    i += 1
                    j = 0

    for i in range(1, max_num + 1):
        goal_state[(i-1)//n][(i-1)%n] = i
    goal_state[n - 1][n - 1] = 0

    puzzle = Puzzle(init_state, goal_state)
    ans = puzzle.solve()

    with open(sys.argv[2], 'a') as f:
        for answer in ans:
            f.write(answer+'\n')


