"""
Tic Tac Toe Player, Project from CS50 Intro to AI course

12/19/2020  Jenny Cao   Version 1.0
    Current Progress: Game is able to function without error. All methods have been implemented
    Remaining Tasks: 1. optimize running time for minimax - alpha beta pruning
                     2. optimize winning rate - if opponent is almost winning, block them!

12/22/2020  Jenny Cao   Version 1.1
    Current Progress: Optimized Null State, with first move at the center
                      Optimized winning rate - implementing minimax algorithm
                        
    Remaining Tasks: 1. optimize running time for minimax - alpha beta pruning

12/31/2020  Jenny Cao   Version 1.2
    Current Progress: Fixed error: in minimax, calling helper functions max or min should correspond to the next move.
                                   In the previous version, minimax has already performed max or min in selecting best-value,
                                   but instead called min or max again, causing moves not optimized
                      Optimized winning rate - included counting depth to calculate overall score

    Remaining Tasks: 1. optimize running time for minimax - alpha beta pruning

1/14/2021   Jenny Cao   Version 1.3
    Current Progress: Implemented alpha-beta pruning, running time noticeably decreased.

    Remaining Tasks: Currently none. Maybe code optimization to improve simplicity and/or readability.
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None

PlayerRecord = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player_info who has the next turn on a board.
    """
    x_num = 0
    o_num = 0

    for rows in board:
        for x in rows:
            if x != EMPTY:
                if x == X:
                    x_num += 1
                else:
                    o_num += 1

    # x_num = board.count(X)
    # o_num = board.count(O)

    if x_num > o_num:
        return O
    else:
        return X
    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    actionss = []

    for rows in range(3):
        for x in range(3):
            if board[rows][x] == EMPTY:
                actionss.append([rows, x])

    return actionss

    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    if len(action) != 2:
        raise ValueError('Incorrect form of action')

    row = action[0]
    col = action[1]

    board_copy = copy.deepcopy(board)

    if board_copy[row][col] != EMPTY:
        raise ValueError('Invalid action')

    board_copy[row][col] = player(board_copy)

    return board_copy

    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    for row in board:
        if row[0] == row[1] == row[2]:
            return row[0]

    for x in range(3):
        if board[0][x] == board[1][x] == board[2][x]:
            return board[0][x]

    if board[0][0] == board[1][1] == board[2][2]: return board[0][0]

    if board[0][2] == board[1][1] == board[2][0]: return board[0][2]

    return None
    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    if utility(board) != 0:
        return True

    for rows in board:
        for x in rows:
            if x == EMPTY:
                return False
    return True
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player_info on the board.
    """

    if terminal(board):
        return None

    if check_null(board):
        return [1, 1]

    current_player = player(board)
    depth = 0
    all_action = actions(board)
    best_action = all_action[0]
    alpha = float("-inf")
    beta = float("inf")

    if player == X:

        best_value = min_value(current_player, result(board, all_action[0]), depth, alpha, beta)

        for a in all_action:
            depth = 0
            current_value = min_value(current_player, result(board, a), depth, alpha, beta)

            if current_value > best_value:
                best_value = current_value
                best_action = a

        return best_action

    else:
        best_value = max_value(current_player, result(board, all_action[0]), depth, alpha, beta)

        for a in all_action:
            depth = 0
            current_value = max_value(current_player, result(board, a), depth, alpha, beta)

            if current_value < best_value:
                best_value = current_value
                best_action = a

        return best_action

    raise NotImplementedError


def check_null(board):
    for rows in range(3):
        for x in range(3):
            if board[rows][x] != EMPTY:
                return False
    return True


def score_check(player_info, board, depth):
    """
    calculate score: if player_info ended up winning or tie, the less steps it takes the better;
                     if player_info ended up losing, the more steps if went through (put up a fight before giving up) the better
    """
    score = utility(board) * 10
    if player_info == X:  # when player_info is X, we want score to be max
        if score == -10:  # when player_info is X but O won
            score = depth + score  # more steps it takes the better
        else:  # when player_info is X and X won
            score = score - depth  # less steps it takes the better
    else:  # when player_info is O, we want score to be min
        if score == 10:  # when player_info is O but X won
            score = score - depth  # more steps it takes the better
        else:  # when player_info is O and O won
            score = depth + score  # less steps it takes the better
    return score


def max_value(player_info, board, depth, alpha, beta):
    depth += 1
    if terminal(board):
        score = score_check(player_info, board, depth)
        return score
    v = float('-inf')

    for act in actions(board):
        v = max(v, min_value(player_info, result(board, act), depth, alpha, beta))
        if v >= beta:
            return v
        alpha = max(alpha, v)
    return v


def min_value(player_info, board, depth, alpha, beta):
    depth += 1
    if terminal(board):
        score = score_check(player_info, board, depth)

        return score
    v = float('inf')

    for act in actions(board):
        v = min(v, max_value(player_info, result(board, act), depth, alpha, beta))
    if v <= alpha:
        return v
    beta = min(beta, v)
    return v
