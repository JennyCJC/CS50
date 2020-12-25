"""
Tic Tac Toe Player

12/19/2020  Jenny Cao   Version 1.0
    Current Progress: Game is able to function without error. All methods have been implemented
    Remaining Tasks: 1. optimize running time for minimax - alpha beta pruning
                     2. optimize winning rate - if opponent is almost winning, block them!

12/22/2020  Jenny Cao   Version 1.1
    Current Progress: Optimized Null State, with first move at the center
                      Optimized winning rate - implementing minimax algorithm
                        
    Remaining Tasks: 1. optimize running time for minimax - alpha beta pruning
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
    Returns player who has the next turn on a board.
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
    #o_num = board.count(O)

    if(x_num > o_num):
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

    if(len(action) != 2):
        raise ValueError('Incorrect form of action')

    row = action[0]
    col = action[1]

    board_copy = copy.deepcopy(board)

    if(board_copy[row][col] != EMPTY):
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
    Returns the optimal action for the current player on the board.
    """

    if terminal(board) == True:
        return None


    if checkNull(board) == True:
        return [1,1]

    allAction = actions(board)
    best_value = max_value(result(board, allAction[0]))
    best_action = allAction[0]
    if player(board) == X:
        for a in allAction:
            current_value = max_value(result(board, a))
            if current_value > best_value:
                best_value = current_value
                best_action = a
        return best_action
    else:
        for a in allAction:
            current_value = min_value(result(board, a))
            if current_value < best_value:
                best_value = current_value
                best_action = a
        return best_action


    '''
    if len(record_X) != 0:
        return record_X[0]
    elif len(record_0) != 0:
        return record_0[0]
    else:
        return record_O[0]
    '''

    raise NotImplementedError

def checkNull(board):
    for rows in range(3):
        for x in range(3):
            if board[rows][x] != EMPTY:
                return False
    return True
'''
def minimaxHelp(board, score, actionlist):
    
    
        for row in range(len(actionlist)):
            if terminal(result(board, actionlist[row])) == False:
                curresult = result(board, actionlist[row])
                minimaxHelp(curresult, score, actions(curresult)) 

            else:
                if utility(board) == 1:
                    score[row] += 1
                elif  utility(board) == 0:
                    score[row] += 0
                else:
                    score[row] += -1
'''
def max_value(board):
    if terminal(board):
        return utility(board)
    v = float('-inf')
   
    for act in actions(board):
        v = max(v, min_value(result(board, act)))
        
    return v

def min_value(board):
    if terminal(board):
        return utility(board)
    v = float('inf')

    for act in actions(board):
        v = min(v, max_value(result(board, act)))
    return v
