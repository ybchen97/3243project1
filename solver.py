import sys

def move_down(puzzle):
    x, y = get_zero(puzzle)
    puzzle[x][y] = puzzle[x - 1][y]
    puzzle[x - 1][y] = 0

def move_up(puzzle):
    x, y = get_zero(puzzle)
    puzzle[x][y] = puzzle[x + 1][y]
    puzzle[x + 1][y] = 0

def move_left(puzzle):
    x, y = get_zero(puzzle)
    puzzle[x][y] = puzzle[x][y + 1]
    puzzle[x][y + 1] = 0 

def move_right(puzzle):
    x, y = get_zero(puzzle)
    puzzle[x][y] = puzzle[x][y - 1]
    puzzle[x][y - 1] = 0

def print_puzzle(puzzle):
    size = len(puzzle)
    for i in range(size):
        print(puzzle[i])

def get_zero(puzzle):
        x, y = None, None
        for i in range(len(puzzle)):
            for j in range(len(puzzle)):
                if puzzle[i][j] == 0:
                    x, y = i, j
                    break
            if x != None:
                break
        return x, y

#arg[0] = name of script
#arg[1] = starting state of puzzle
#arg[2] = list of moves, each move should be in a new line
if len(sys.argv) != 3:
    raise ValueError("Wrong number of arguments!")

with open(sys.argv[1], 'r') as f:
    lines = f.readlines()

n = len(lines)
max_num = n ** 2 - 1

puzzle = [[0 for i in range(n)] for j in range(n)]

i,j = 0, 0
for line in lines:
    for number in line.split(" "):
        if number == '':
            continue
        value = int(number , base = 10)
        if  0 <= value <= max_num:
            puzzle[i][j] = value
            j += 1
            if j == n:
                i += 1
                j = 0

with open(sys.argv[2], 'r') as g:
    moves = g.readlines()
    for i in range(len(moves)):
        moves[i] = moves[i].rstrip('\n')

print("Original state:")
print_puzzle(puzzle)

if moves[0] == "UNSOLVABLE":
    print("The puzzle cannot be solved.")
else:
    for k in range(len(moves)):
        if moves[k] == "DOWN":
            print("Move: DOWN")
            move_down(puzzle)
        elif moves[k] == "UP":
            print("Move: UP")
            move_up(puzzle)
        elif moves[k] == "LEFT":
            print("Move: LEFT")
            move_left(puzzle)
        else:
            print("Move: RIGHT")
            move_right(puzzle)
        print_puzzle(puzzle)