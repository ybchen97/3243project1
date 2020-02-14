import os
import sys
import copy
import math
from collections import deque


class Puzzle(object):
    def __init__(self, init_state, goal_state):
        # you may add more attributes if you think is useful
        self.init_state = self.stringify(init_state)
        self.goal_state = self.stringify(goal_state)
        self.actions = ["DOWN", "UP", "RIGHT", "LEFT"]
        self.size = len(init_state)

    def solve(self):
        #TODO
        if self.grid_parity(self.init_state) != self.grid_parity(self.goal_state):
            return ['UNSOLVABLE']
        # implement your search algorithm here
        frontier = deque([self.init_state])
        frontier_set = set([self.init_state])
        visited = set()
        parent = {self.init_state: (None, None)} #(prev_state, direction)
        reached_goal = False
        if self.init_state == self.goal_state:
            reached_goal = True

        while len(frontier) > 0 and not reached_goal:
            current_state = frontier.popleft()
            frontier_set.remove(current_state)
            visited.add(current_state)
            position = self.get_zero(current_state)

            for a in self.actions:
                new_state = self.move(current_state, a, position)
                if new_state != None and new_state not in visited and new_state not in frontier_set:
                    parent[new_state] = (current_state, a)

                    # check goal state here to skip processing of nodes in queue
                    if new_state  == self.goal_state:
                        reached_goal = True
                        break

                    frontier.append(new_state)
                    frontier_set.add(new_state)

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
            state += "".join([chr(j + ord('A')) for j in grid[i]])
        return state

    def grid_parity(self, state):
        next = [-1] * len(state)
        count = 0
        for i in state:
            num = ord(i) - ord('A')
            if next[num] != -1:
                continue
            count += 1
            j = num
            while ord(state[j]) - ord('A') != num:
                next[j] = ord(state[j]) - ord('A')
                j = next[j]
            next[j] = ord(state[j]) - ord('A')
        if self.size % 2 == 1:
            return (len(state) - 1 - count) % 2
        else:
           return (len(state) - 1 - count + len(state) // self.get_zero(state)) % 2
        
        

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







