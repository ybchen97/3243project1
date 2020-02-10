import os
import sys
import copy
import random
import heapq
import math


class Puzzle(object):
    def __init__(self, init_state, goal_state):
        # you may add more attributes if you think is useful
        self.init_state = self.stringify(init_state)
        self.goal_state = self.stringify(goal_state)
        self.actions = ["DOWN", "UP", "RIGHT", "LEFT"]
        self.size = int(math.sqrt(len(self.init_state)))

    def solve(self):
        #TODO
        # implement your search algorithm here
        initial_evaluation = self.calculate_evaluation_function(self.init_state, 0)

        # Frontier nodes stored as (evaluation_cost, current_state, actual_cost) 
        frontier = [(initial_evaluation, self.init_state, 0)] 

        # Visited stores a key-value pair, with the key being the state of the grid and value being the current lowest 
        # value calculated by the evaluation function
        visited = {self.init_state: initial_evaluation}
        parent = {self.init_state: (None, None)} #(prev_state, direction)
        reached_goal = False
        if self.init_state == self.goal_state:
            reached_goal = True

        while len(frontier) > 0 and not reached_goal:
            # Removes the current node
            current_node = heapq.heappop(frontier)
            current_state = current_node[1]

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

                            # check goal state here to skip processing of nodes in queue
                            if new_state == self.goal_state:
                                reached_goal = True
                                break

                            visited[new_state] = evaluation_cost
                            heapq.heappush(frontier, (evaluation_cost, new_state, actual_cost))

        final_answer = []
        backtrack_state = self.goal_state
        while backtrack_state in parent and backtrack_state != self.init_state:
            final_answer.insert(0, parent[backtrack_state][1])
            backtrack_state = parent[backtrack_state][0]

        print("Length of visited: {0}".format(len(visited)))
        return ['UNSOLVABLE'] if not reached_goal else final_answer

    # you may add more functions if you think is useful
    def stringify(self, grid):
        # 65 == A, 0 -> A, 1 -> B ...
        state = ""
        for i in range(len(grid)):
            state += "".join([chr(j + 65) for j in grid[i]])
        return state

    def move(self, state, dir, pos):
        new_state = list(state)
        if dir == "DOWN" and pos > (self.size - 1):
            new_state[pos], new_state[pos - self.size] = new_state[pos - self.size], new_state[pos]
            new_state = "".join(new_state)
        elif dir == "UP" and pos < (len(state) - self.size):
            new_state[pos], new_state[pos + self.size] = new_state[pos + self.size], new_state[pos]
            new_state = "".join(new_state)
        elif dir == "RIGHT" and (pos % self.size) != 0:
            new_state[pos], new_state[pos - 1] = new_state[pos - 1], new_state[pos]
            new_state = "".join(new_state)
        elif dir == "LEFT" and (pos % self.size) != (self.size - 1):
            new_state[pos], new_state[pos + 1] = new_state[pos + 1], new_state[pos]
            new_state = "".join(new_state)
        else:
            return None
        return new_state
    
    def get_zero(self, grid):
        return grid.index("A")

    def calculate_manhattan_distance(self, grid):
        manhattan_distance = 0
        for i, letter in enumerate(grid):
            x = i % self.size
            y = i // self.size
            if letter == "A":
                manhattan_distance += abs(self.size - 1 - y) + abs(self.size - 1 - x)
            else:
                num = ord(letter) - 65
                x_change = abs( (num - 1) % self.size - x)
                y_change = abs( (num - 1) // self.size - y)
                manhattan_distance += x_change + y_change
        return manhattan_distance

    def calculate_evaluation_function(self, grid, current_cost):
        return self.calculate_manhattan_distance(grid) + current_cost

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







