import random, time
N = 10000
MAX = 100000
rows_conflicts = dict()
left_diagonals = dict()
right_diagonals = dict()


def random_pos(list, filter):
    return random.choice([i for i in range(N) if filter(i)])


def gen_board(n):
    board = []
    for i in range(n):
        board.append(random.randint(0, n - 1))
    return board


def gen_staches(board):
    for column, row in enumerate(board):
        rows_conflicts[row] += 1
        right_diagonals[row + column] += 1
        left_diagonals[row - column] += 1


def init_staches():
    for i in range(N):
        rows_conflicts[i] = 0

    for i in range(2*N - 1):
        right_diagonals[i] = 0

    for i in range(-N + 1, N):
        left_diagonals[i] = 0


def least_conflicts(board, column):
    row_original = board[column]
    rows_conflicts[row_original] -= 1
    right_diagonals[row_original + column] -= 1
    left_diagonals[row_original - column] -= 1

    conflicts = []

    for row in range(N):
        conflict = rows_conflicts[row] + right_diagonals[row + column] + left_diagonals[row - column]
        conflicts.append(conflict)

    minimum = min(conflicts)

    min_conflicts_idx = []
    for i in range(len(conflicts)):
        if conflicts[i] == minimum:
            min_conflicts_idx.append(i)

    choice = random.choice(min_conflicts_idx)
    rows_conflicts[choice] += 1
    right_diagonals[choice + column] += 1
    left_diagonals[choice - column] += 1

    return choice


def is_solved():
    for conflict in list(rows_conflicts.values()):
        if conflict > 1:
            return False

    for conflict in list(right_diagonals.values()):
        if conflict > 1:
            return False

    for conflict in list(left_diagonals.values()):
        if conflict > 1:
            return False

    return True


def solve(n, max_iter):
    board = gen_board(n)
    init_staches()
    gen_staches(board)
    while not is_solved():
        for i in range(max_iter):
            column = random_pos(board, lambda column: rows_conflicts[board[column]] + right_diagonals[board[column] + column] + left_diagonals[board[column] - column] > 3)
            row = least_conflicts(board, column)
            board[column] = row

            if is_solved():
                return board
        board = gen_board(n)
        init_staches()
        gen_staches(board)


start = time.time()
solve(N, MAX)
end = time.time()
print(end - start)




