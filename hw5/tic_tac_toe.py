from copy import deepcopy
import random
import os
import platform

clear = "clear"

if platform.system() == "Windows":
    clear = "cls"

LOSE = -1
WIN = 1
DRAW = 0
WIN_X = ["X", "X", "X"]
WIN_O = ["O", "O", "O"]
EMPTY = "_"
WIN_X_TUPLE = tuple(WIN_X)
WIN_O_TUPLE = tuple(WIN_O)
MINUS_INFINITY = -2
INFINITY = 2

def check_end_game(board):
    transposed = list(zip(*board))
    if WIN_X in board or WIN_X_TUPLE in transposed:
        return "X"
    if WIN_O in board or WIN_O_TUPLE in transposed:
        return "O"

    # diagonals
    if board[0][0] != EMPTY and board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]

    if board[0][2] != EMPTY and board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]

    for row in board:
        if EMPTY in row:
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

def alpha_beta(board, player, ai_player, other_player, alpha, beta):
    end_game = check_end_game(board)
    if end_game is not None:
        if end_game == ai_player:
            return WIN
        elif end_game == other_player:
            return LOSE
        else:
            return DRAW

    if player == ai_player:
        next_player = other_player
    else:
        next_player = ai_player

    if player == ai_player:
        v = MINUS_INFINITY
        for new_board in get_possible_boards(board, player):
            v = max(v, alpha_beta(new_board, next_player, ai_player, other_player, alpha, beta))
            alpha = max(alpha, v)
            if v == WIN:
                break
            if beta <= alpha:
                break
        return v
    else:
        v = INFINITY
        for new_board in get_possible_boards(board, player):
            v = min(v, alpha_beta(new_board, next_player, ai_player, other_player, alpha, beta))
            beta = min(beta, v)
            if v == LOSE:
                break
            if beta <= alpha:
                break
        return v

def make_decision(board, ai_player, other_player):
    boards_evaluation = []
    for new_board in get_possible_boards(board, ai_player):
        boards_evaluation.append((new_board, alpha_beta(new_board, other_player, ai_player, other_player, MINUS_INFINITY, INFINITY)))
    m = max(boards_evaluation, key=lambda cost: cost[1])
    # choose at random one of the best moves so as to not play the same way every time
    return random.choice([x for x in boards_evaluation if x[1] == m[1]])


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
    #pick at random who will play first
    start = random.randint(0, 1)
    if start == 1:
        ai_player = "X"
        other_player = "O"
    else:
        ai_player = "O"
        other_player = "X"
    turns = ["X", "O"]
    turn = 0
    while True:
        os.system(clear)
        print_board(board)
        if turns[turn % 2] == other_player:
            print("It's player's turn({0})".format(other_player))
            x = -1
            y = -1
            while not correct_input(x, y, board):
                x, y = list(map(int, input().split()))
                x -= 1
                y -= 1
            board[x][y] = other_player
        else:
            print("It's computer's turn({0})".format(ai_player))
            board_new, cost = make_decision(board, ai_player, other_player)
            board = board_new
        turn += 1
        winner = check_end_game(board)
        if winner is not None:
            os.system(clear)
            print_board(board)
            if winner == ai_player:
                print("Computer won!")
            elif winner == other_player:
                print("You won!")
            else:
                print("It's a draw")
            break

play()
