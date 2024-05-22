"""
Tic Tac Toe Player
"""
import copy
import math

X = "X"
O = "O"
EMPTY = None


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
    x_count = 0
    o_count = 0

    for row in board:
        for cell in row:
            if cell != EMPTY:
                if cell == X:
                    x_count += 1
                else:
                    o_count += 1

    if o_count < x_count:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))

    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception("Invalid action")

    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check rows
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != EMPTY:
            return row[0]

    # Check columns
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != EMPTY:
            return board[0][i]

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != EMPTY:
        return board[0][2]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True

    for row in board:
        for cell in row:
            if cell == EMPTY:
                return False

    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)

    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    if board == initial_state() and player(board) == X:
        return 0, 0

    optimal_action = actions(board).pop()
    optimal_result = float('-inf') if player(board) == X else float('inf')

    if player(board) == X:
        for action in actions(board):
            v = max_value(result(board, action), optimal_result)
            if v > optimal_result:
                optimal_result = v
                optimal_action = action
    else:
        for action in actions(board):
            v = min_value(result(board, action), optimal_result)
            if v < optimal_result:
                optimal_result = v
                optimal_action = action

    return optimal_action


def max_value(board, prev_max):
    if terminal(board):
        return utility(board)

    v = float('-inf')
    for action in actions(board):
        v = max(v, min_value(result(board, action), prev_max))
        if v > prev_max:
            return v
    return v


def min_value(board, prev_min):
    if terminal(board):
        return utility(board)

    v = float('inf')
    for action in actions(board):
        v = min(v, max_value(result(board, action), prev_min))
        if v < prev_min:
            return v

    return v
