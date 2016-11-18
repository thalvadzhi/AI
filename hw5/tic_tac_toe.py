from copy import deepcopy
import random
import os
import platform
if platform.system() == "Linux":
    clear = "clear"
elif platform.system() == "Windows":
    clear = "cls"

LOSE = -1
WIN = 1
DRAW = 0
WIN_X = ["X", "X", "X"]
WIN_O = ["O", "O", "O"]
EMPTY = "_"
AI_PLAYER = "X"
OTHER_PLAYER = "O"

WIN_X_TUPLE = tuple(WIN_X)
WIN_O_TUPLE = tuple(WIN_O)

def check_end_game(board):
    transposed = list(zip(*board))
    if WIN_X in board or WIN_X_TUPLE in transposed:
        return "X"
    if WIN_O in board or WIN_O_TUPLE in transposed:
        return "O"

    # diagonals

    if board[0][0] != EMPTY and board[0][0] == board[1][1] == board[2][2] :
        return board[0][0]

    if board[0][2] != EMPTY and board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]

    for i in range(3):
        for k in range(3):
            if board[i][k] == EMPTY:
                return None

    return "D"


def get_possible_boards(board, player):
    boards = []
    for i in range(3):
        for k in range(3):
            if board[i][k] == EMPTY:
                new_board = deepcopy(board)
                new_board[i][k] = player
                boards.append(new_board)
    return boards

next_move = []


def minimax(board, player, AI_PLAYER, OTHER_PLAYER):
    end_game = check_end_game(board)
    if end_game is not None:
        if end_game == AI_PLAYER:
            return WIN
        elif end_game == OTHER_PLAYER:
            return LOSE
        else:
            return DRAW

    values = []

    if player == AI_PLAYER:
        next_player = OTHER_PLAYER
    else:
        next_player = AI_PLAYER

    for new_board in get_possible_boards(board, player):
        x = minimax(new_board, next_player, AI_PLAYER, OTHER_PLAYER)

        values.append(x)
        if player == AI_PLAYER:
            if x == WIN:
                break
        else:
            if x == LOSE:
                break

    if player == AI_PLAYER:
        max_value = max(values)
        return max_value
    else:
        return min(values)


def minimaxi(board, player, AI_PLAYER, OTHER_PLAYER):
    val = []
    for new_board in get_possible_boards(board, player):
        val.append((new_board, minimax(new_board, OTHER_PLAYER, AI_PLAYER, OTHER_PLAYER)))
    m = max(val, key=lambda  cost: cost[1])
    return random.choice([x for x in val if x[1] == m[1]])
    # return max(val, key=lambda cost: cost[1])


def correct_input(x, y, board):
    if x > 2 or y > 2 or x < 0 or y < 0:
        return False
    if board[x][y] != "_":
        return False
    return True

def print_board(board):
    for row in board:
        print(" ".join(row))

def play():

    board = [["_"] * 3 for _ in range(3)]

    start = random.randint(0, 1)
    if start == 1:
        AI_PLAYER = "X"
        OTHER_PLAYER = "O"
        turns = [AI_PLAYER, OTHER_PLAYER]
    else:
        AI_PLAYER = "O"
        OTHER_PLAYER = "X"
        turns = [OTHER_PLAYER, AI_PLAYER]
    turn = 0

    while True:
        os.system(clear)
        print_board(board)
        if turns[turn % 2] == OTHER_PLAYER:
            print("It's player's turn(" + OTHER_PLAYER + ")")
            x, y = list(map(int, input().split()))
            while not correct_input(x, y, board):
                x, y = list(map(int, input().split()))
            board[x][y] = OTHER_PLAYER
        else:
            print("It's computer's turn(" + AI_PLAYER + ")")
            board_new, cost = minimaxi(board, AI_PLAYER, AI_PLAYER, OTHER_PLAYER)
            board = board_new
        turn += 1
        b = check_end_game(board)
        if b != None:
            os.system(clear)
            print_board(board)
            if b == AI_PLAYER:
                print("Computer won!")
            elif b == OTHER_PLAYER:
                print("You won!")
            else:
                print("It's a draw")
            break

play()

