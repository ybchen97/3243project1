import os
import sys
import copy
import random
import heapq


class Puzzle(object):
    def __init__(self, init_state, goal_state):
        # you may add more attributes if you think is useful
        self.init_state = init_state
        self.goal_state = goal_state
        self.actions = ["DOWN", "UP", "RIGHT", "LEFT"]
        self.size = len(init_state)

    def solve(self):
        #TODO
        # implement your search algorithm here
        initial_evaluation = self.calculate_evaluation_function(self.init_state, 0)
        # Frontier nodes stored as (evaluation_cost, current_state, actual_cost) 
        frontier = [(initial_evaluation, self.init_state, 0)] 
        # Visited stores a key-value pair, with the key being the state of the grid and value being the current lowest 
        # value calculated by the evaluation function
        visited = {str(self.init_state): initial_evaluation}
        parent = {str(self.init_state): (None, None)} #(prev_state, direction)

        while len(frontier) > 0:
            # Removes the current node
            current_node = heapq.heappop(frontier)
            current_state = current_node[1]
            current_state_string= str(current_state)
            # Checks if the current node has the updated lower evaluation value
            if (current_state_string in visited and visited[current_state_string] == current_node[0]) :
                if current_state == goal_state:
                    break  
                x, y = self.get_zero(current_state)

                random.shuffle(self.actions)
                for a in self.actions:
                    new_state = self.move(current_state, a, x, y)
                    if new_state != None:
                        actual_cost = current_node[2] + 1 # Updates the actual cost required to get to current node
                        evaluation_cost = self.calculate_evaluation_function(new_state, actual_cost)
                        new_state_string = str(new_state)
                        if (new_state_string in visited and evaluation_cost < visited[new_state_string]) or (new_state_string not in visited):
                            # Node is only added into the frontier if the new evaluation cost is lower or has not been visited
                            visited[new_state_string] = evaluation_cost
                            heapq.heappush(frontier, (evaluation_cost, new_state, actual_cost))
                            parent[str(new_state)] = (current_state, a)
                    

        final_answer = []
        backtrack_state = self.goal_state
        while str(backtrack_state) in parent and backtrack_state != self.init_state:
            final_answer.insert(0, parent[str(backtrack_state)][1])
            backtrack_state = parent[str(backtrack_state)][0]

        print(len(visited))
        return ['UNSOLVABLE'] if len(final_answer) == 0 else final_answer

    # you may add more functions if you think is useful
    def move(self, grid, dir, x, y):
        new_state = copy.deepcopy(grid)
        if dir == "DOWN" and x > 0:
            new_state[x][y], new_state[x - 1][y] = new_state[x - 1][y], 0
        elif dir == "UP" and x < self.size - 1:
            new_state[x][y], new_state[x + 1][y] = new_state[x + 1][y], 0
        elif dir == "RIGHT" and y > 0:
            new_state[x][y], new_state[x][y - 1] = new_state[x][y - 1], 0
        elif dir == "LEFT" and y < self.size - 1:
            new_state[x][y], new_state[x][y + 1] = new_state[x][y + 1], 0
        else:
            return None
        return new_state

    def get_zero(self, grid):
        x, y = None, None
        for i in range(self.size):
            for j in range(self.size):
                if grid[i][j] == 0:
                    x, y = i, j
                    break
            if x != None:
                break
        return x, y
    

    def calculate_manhattan_distance(self, grid):
        manhattan_distance = 0
        for i in range(self.size):
            for j in range(self.size):
                if grid[i][j] == 0:
                    manhattan_distance += abs(self.size - 1 - j) + abs(self.size - 1 - i)
                else:
                    x_change = abs( (grid[i][j] - 1) % self.size - j)
                    y_change = abs( (grid[i][j] - 1) // self.size - i)
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







