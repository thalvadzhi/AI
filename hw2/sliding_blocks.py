import queue, math
from copy import copy, deepcopy
import time
n = 5


def gen_target_board():
    i = 1
    target_board = []
    for j in range(n):
        target_board.append([])
        for k in range(n):
            target_board[j].append(i)
            i += 1
    target_board[n - 1][n - 1] = 0
    return target_board


def gen_target_coordinages(target):
    target_coordinates = dict()
    for i in range(n):
        for j in range(n):
            target_coordinates[target[i][j]] = (i, j)
    return target_coordinates


target = gen_target_board()
coordinates = gen_target_coordinages(target)
inheritance = dict()


def gen_possible_moves(current):
    #first find the empty element
    x, y = -1, -1
    for i in range(n):
        for j in range(n):
            if current[i][j] == 0:
                x, y = i, j


    all_moves = []
    if x + 1 < n:
        current_copy = deepcopy(current)
        current_copy[x][y], current_copy[x + 1][y] = current_copy[x + 1][y], current_copy[x][y]
        all_moves.append(current_copy)

    if x - 1 >= 0:
        current_copy = deepcopy(current)
        current_copy[x][y], current_copy[x - 1][y] = current_copy[x - 1][y], current_copy[x][y]
        all_moves.append(current_copy)

    if y + 1 < n:
        current_copy = deepcopy(current)
        current_copy[x][y], current_copy[x][y + 1] = current_copy[x][y + 1], current_copy[x][y]
        all_moves.append(current_copy)

    if y - 1 >= 0:
        current_copy = deepcopy(current)
        current_copy[x][y], current_copy[x][y - 1] = current_copy[x][y - 1], current_copy[x][y]
        all_moves.append(current_copy)

    return all_moves


def calculate_heuristic(board):
    sum = 0
    for i in range(n):
        for k in range(n):
            #those are the target coordinates
            x, y = coordinates[board[i][k]]
            sum += math.fabs(x - i) + math.fabs(y - k)
    return sum



def find_solution(input_board):
    visited = set()
    q = queue.PriorityQueue()
    h = calculate_heuristic(input_board)
    q.put((h, input_board))
    visited.add(str(input_board))
    while not q.empty():
        h, elem = q.get()
        visited.add(str(elem))
        if elem == target:
            steps = []
            steps.append(str(elem))
            parent = inheritance[str(elem)]
            while parent != str(input_board):
                steps.append(parent)
                parent = inheritance[parent]
            steps.append(str(input_board))
            steps.reverse()
            return steps
        for move in gen_possible_moves(elem):
            if str(move) not in visited:
                inheritance[str(move)] = str(elem)
                q.put((calculate_heuristic(move), move))


input = [[14,3,4,8],
         [5,11,7,10],
         [9,1,12,15],
         [2,13,6,0]]

# input = [[2,6,1],[7,4,0],[5,3,8]]
def print_pretty(steps):
    for step in steps:
        step_str = ""
        for row in step:
            step_str += str(row) + "\n"
            print(step_str)
        print("\n")
input3 = [[1,13,10,18,4],[7,24,2,14,20],[16,0,17,5,11],[9,12,3,6,19],[22,21,23,8,15]]
start = time.time()
find_solution(input3)
end = time.time()
print(end - start)


