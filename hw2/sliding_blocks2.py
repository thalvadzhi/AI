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
        all_moves.append(current)

    if empty_index >= n:
        #above
        current = board[:]
        current[empty_index], current[empty_index - n] = current[empty_index - n], current[empty_index]
        all_moves.append(current)

    if empty_index % n:
        #left
        current = board[:]
        current[empty_index], current[empty_index -1] = current[empty_index - 1], current[empty_index]
        all_moves.append(current)

    if empty_index % n != n - 1:
        #right
        current = board[:]
        current[empty_index], current[empty_index + 1] = current[empty_index + 1], current[empty_index]
        all_moves.append(current)

    return all_moves

inheritance = dict()
def find_solution(input_board):
    visited = set()
    q = queue.PriorityQueue()
    h = calc_heuristic(input_board)
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
        for move in find_possible_moves(elem):
            if str(move) not in visited:
                inheritance[str(move)] = str(elem)
                q.put((calc_heuristic(move), move))
# input = [2,6,1,
#          7,4,0,
#          5,3,8]
input2 = [1,2,3,4,5,6,0,7,8]
input = [14,3,4,8,5,11,7,10,9,1,12,15,2,13,6,0]
input1 = [0,10,7,4,8,5,6,12,11,2,1,15,9,13,3,14]
input3 = [1,13,10,18,4,7,24,2,14,20,16,0,17,5,11,9,12,3,6,19,22,21,23,8,15]
start = time.time()
find_solution(input1)
end = time.time()
print(end - start)