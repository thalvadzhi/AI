import math, queue
import time
N = 15
n = 4
target = list(range(1, N + 1))
target.append(0)

def calc_heuristic(board):
    sum = 0
    for index, elem in enumerate(board):
        target_index = target.index(elem)
        actual_x_target = target_index % n
        actual_y_target = math.floor(target_index / n)

        actual_x_current = index % n
        actual_y_current = math.floor(index / n)

        sum += math.fabs(actual_x_current - actual_x_target) + math.fabs(actual_y_current - actual_y_target)
    return sum


def find_possible_moves(board):
    empty_index = board.index(0)
    all_moves = []
    if empty_index + n < N+1:
        #below
        current = board[:]
        current[empty_index], current[empty_index + n] = current[empty_index + n], current[empty_index]
        all_moves.append((current, "up"))

    if empty_index >= n:
        #above
        current = board[:]
        current[empty_index], current[empty_index - n] = current[empty_index - n], current[empty_index]
        all_moves.append((current, "down"))

    if empty_index % n:
        #left
        current = board[:]
        current[empty_index], current[empty_index -1] = current[empty_index - 1], current[empty_index]
        all_moves.append((current, "right"))

    if empty_index % n != n - 1:
        #right
        current = board[:]
        current[empty_index], current[empty_index + 1] = current[empty_index + 1], current[empty_index]
        all_moves.append((current, "left"))

    return all_moves

def find_solution(input_board):
    inheritance = dict()
    visited = set()
    q = queue.PriorityQueue()
    h = calc_heuristic(input_board)
    q.put((h, (input_board, "")))
    visited.add(str(input_board))
    path_length = dict()
    path_length[str(input_board)] = 0
    while not q.empty():
        h, elem = q.get()
        elem_board, elem_command = elem
        elem_str = str(elem_board)
        visited.add(elem_str)
        if elem_board == target:
            steps = []
            steps.append(elem_command)
            parent = inheritance[(str(elem_board), elem_command)]
            parent_board, parent_command = parent
            while parent_board != str(input_board):
                steps.append(parent_command)
                parent = inheritance[parent]
                parent_board, parent_command = parent
            #steps.append(str(input_board))
            steps.reverse()
            return steps
        for move in find_possible_moves(elem_board):
            board, command = move
            move_str = str(board)
            for_inh_parent = (str(elem_board), elem_command)
            if move_str not in visited:
                path_length[move_str] = path_length[elem_str] + 1
                for_inh = (str(board), command)
                inheritance[for_inh] = for_inh_parent
                q.put((calc_heuristic(board) + path_length[move_str], move))
# input = [2,6,1,
#          7,4,0,
#          5,3,8]
input2 = [1,2,3,4,5,6,0,7,8]
input = [14,3,4,8,5,11,7,10,9,1,12,15,2,13,6,0]
input1 = [0,10,7,4,8,5,6,12,11,2,1,15,9,13,3,14]
input3 = [1,13,10,18,4,7,24,2,14,20,16,0,17,5,11,9,12,3,6,19,22,21,23,8,15]
input4 = [2,9,10,14,8,0,11,1,15,4,7,5,3,6,13,12]
input5 = [1,11,6,10,13,2,3,4,15,9,7,8,14,0,12,5]
start = time.time()
m = find_solution(input5)
print(len(m))
print(m)
end = time.time()
print(end - start)