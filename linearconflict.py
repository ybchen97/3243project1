import sys
import random
import heapq
import math


class Puzzle(object):
    def __init__(self, init_state, goal_state):
        # you may add more attributes if you think is useful
        self.size = len(init_state) # size refers to the dimension of the grid
        self.init_state = self.flatten(init_state)
        self.goal_state = self.flatten(goal_state)
        self.actions = ["DOWN", "UP", "RIGHT", "LEFT"]
        
        # This is to keep track of the metrics for evaluation of performance
        # self.time_taken = 0
        self.number_of_nodes_expanded = 0
        self.size_of_frontier = 0
        self.number_of_steps = 0

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
                self.number_of_nodes_expanded += 1

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

        # keep track of stats
        self.size_of_frontier = len(visited)
        self.number_of_steps = len(final_answer)
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

    def calculate_manhattan_distance(self, state):
        manhattan_distance = 0
        for i, number in enumerate(state):
            x = i % self.size   # Retrieves the x coordinate of the tile in the original grid
            y = i // self.size  # Retrieves the y coordinate of the tile in the original grid
            if number == 0:
                # Need not account for the blank tile in the heuristic calculation
                continue
            else:
                x_change = abs( (number - 1) % self.size - x)
                y_change = abs( (number - 1) // self.size - y)
                manhattan_distance += x_change + y_change
        return manhattan_distance

    # Returns the goal row and position of the tile
    def calculate_goal_pos(self, tile):
        if tile == 0:
            return self.size - 1, self.size - 1
        else:
            return (tile - 1) // self.size, (tile - 1) % self.size

    # For tiles A and B, we say that A and B form a conflict inversion if the following holds:
    # 1. current position of A > current position of B and goal position of A < goal position of B
    # OR
    # 2. current position of B > current position of A and goal position of B < goal position of A
    # This definition is essentially part of the definition of linear conflict. Extracted it out to make coding simpler.
    def is_conflict_inversion(self, A_current_pos, A_goal_pos, B_current_pos, B_goal_pos):
        return (A_current_pos > B_current_pos and A_goal_pos < B_goal_pos) \
            or (B_current_pos > A_current_pos and B_goal_pos < A_goal_pos)

    # The function below calculates the number of conflicting tiles each tile in the given row has.
    def calculate_conflict_for_single_row(self, state, row_num):
        row_start = self.size * row_num
        row_conflict = [0] * self.size

        for i in range(self.size):
            tile_A = state[row_start + i]
            tile_A_goal_row, tile_A_goal_col = self.calculate_goal_pos(tile_A)
            # We only consider non-blank tiles whose goal row is the current row.
            if tile_A != 0 and tile_A_goal_row == row_num: 
                for j in range(i + 1, self.size):
                    tile_B = state[row_start + j]
                    tile_B_goal_row, tile_B_goal_col = self.calculate_goal_pos(tile_B)
                    # We only consider nonblank tiles whose goal row is the current row and are in conflict inversion with tile A
                    if tile_B != 0 and tile_B_goal_row == row_num and self.is_conflict_inversion(i, tile_A_goal_col, j, tile_B_goal_col):
                        # Once it reaches here, it means that tiles A and B are in linear conflict.
                        # Thus, the number of conflicting tiles for A and B must both increase by 1.
                        row_conflict[i] += 1
                        row_conflict[j] += 1

        return row_conflict

    # The function below calculates the number of conflicts for each tile in a given column.
    def calculate_conflict_for_single_col(self, state, col_num):
        col_conflict = [0] * self.size

        for i in range(self.size):
            tile_A = state[i * self.size + col_num]
            tile_A_goal_row, tile_A_goal_col = self.calculate_goal_pos(tile_A)
            # Similar to the conflict for single row, we only consider non-blank tiles whose goal column is the current column.
            if tile_A != 0 and tile_A_goal_col == col_num:
                for j in range(i + 1, self.size):
                    tile_B = state[j * self.size + col_num]
                    tile_B_goal_row, tile_B_goal_col = self.calculate_goal_pos(tile_B)
                    # We only consider non-blank tiles whose goal column is the current column and are in conflict inversion with tile A.
                    if tile_B != 0 and tile_B_goal_col == col_num and self.is_conflict_inversion(i, tile_A_goal_row, j, tile_B_goal_row):
                        col_conflict[i] += 1
                        col_conflict[j] += 1

        return col_conflict

    # This function helps to calculate the minimum number of tiles required to resolve the linear conflict in the given row.
    def resolve_linear_conflict_for_single_row(self, state, row_num):
        row_conflict = self.calculate_conflict_for_single_row(state, row_num)
        minimum_num_needed = 0
        row_start = row_num * self.size

        # We continue the loop as long as there are still tiles in conflict
        while max(row_conflict) != 0:
            # We identify the largest possible conflict and the column associated to it.
            most_conflicted = max(row_conflict)
            index_of_most_conflicted = row_conflict.index(most_conflicted)
            # After which, we remove the tile with the most conflicts. This reduces its associated conflict to 0.
            row_conflict[index_of_most_conflicted] = 0

            # We denote the most conflicted tile as tile A
            tile_A = state[row_num * self.size + index_of_most_conflicted]
            tile_A_goal_row, tile_A_goal_col = self.calculate_goal_pos(tile_A)

            # We need not check if tile A is the blank tile since the number of conflicts it has is 0. 
            # If the maximum of the row conflict is 0, then it would have exited. Otherwise, there is some non-blank
            # tile in conflict with other tiles.
            for i in range(self.size):
                tile_B = state[row_start + i]
                tile_B_goal_row, tile_B_goal_col = self.calculate_goal_pos(tile_B)
                # At this point, we wish to find tiles that are conflicted with the removed tile in order to decrease
                # the number of tiles it is in conflict with. So, we check for the following
                # 1. the tile is not blank
                # 2. the tile is still in conflict with some other tiles
                # 3. the tile is in linear conflict with the removed tile
                if tile_B != 0 and row_conflict[i] != 0 and tile_B_goal_row == row_num  \
                    and self.is_conflict_inversion(index_of_most_conflicted, tile_A_goal_col, i, tile_B_goal_col):
                    row_conflict[i] -= 1

            minimum_num_needed += 1

        return minimum_num_needed 

    # This function helps to calculate the minimum number of tiles required to resolve the linear conflict in the given column.
    def resolve_linear_conflict_for_single_col(self, state, col_num):
        col_conflict = self.calculate_conflict_for_single_col(state, col_num)
        minimum_num_needed = 0

        # Continue the loop as long as there are still conflicts in the column
        while max(col_conflict) != 0:
            # We identify the most conflicted tile in the column and the row associated to it.
            most_conflicted = max(col_conflict)
            index_of_most_conflicted = col_conflict.index(most_conflicted)
            # After which, we remove this tile. This reduces its associated conflict to 0.
            col_conflict[index_of_most_conflicted] = 0

            # Denote the most conflicted tile as tile A
            tile_A = state[self.size * index_of_most_conflicted + col_num]
            tile_A_goal_row, tile_A_goal_col = self.calculate_goal_pos(tile_A)

            # We need not check if tile A is the blank tile since the number of conflicts it has is 0. 
            # If the maximum of the row conflict is 0, then it would have exited. Otherwise, there is some non-blank
            # tile in conflict with other tiles.
            for i in range(self.size):
                tile_B = state[i * self.size + col_num]
                tile_B_goal_row, tile_B_goal_col = self.calculate_goal_pos(tile_B)
                # At this point, we wish to find tiles that are conflicted with the removed tile in order to decrease
                # the number of tiles it is in conflict with. So, we check for the following
                # 1. the tile is not blank
                # 2. the tile is still in conflict with some other tiles
                # 3. the tile is in linear conflict with the removed tile
                if tile_B != 0 and col_conflict[i] != 0 and tile_B_goal_col == col_num \
                    and self.is_conflict_inversion(index_of_most_conflicted, tile_A_goal_row, i, tile_B_goal_row):
                    col_conflict[i] -= 1
        
            minimum_num_needed += 1
    
        return minimum_num_needed
    
    def calculate_linear_conflict_value(self, state):
        value = 0

        for i in range(self.size):
            value += self.resolve_linear_conflict_for_single_row(state, i)
            value += self.resolve_linear_conflict_for_single_col(state, i)

        return 2 * value

    def calculate_evaluation_function(self, state, current_cost):
        return self.calculate_manhattan_distance(state) + self.calculate_linear_conflict_value(state) + current_cost

    # This function returns a list of [number_of_nodes_expanded, size_of_frontier, number_of_steps]
    def get_statistics(self):
        return [self.number_of_nodes_expanded, self.size_of_frontier, self.number_of_steps]

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






