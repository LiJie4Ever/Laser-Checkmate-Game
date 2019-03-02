from collections import namedtuple
import copy

GameState = namedtuple('GameState', 'to_move board')
infinity = float('inf')
layer = 0


def read_file(file_name):
    with open(file_name, "r") as file:
        next(file)
        board = []
        for line in file:
            line = line.rstrip('\n').strip('\r')
            row = [int(num) for num in line]
            board.append(row)
    return board


def actions(state):
    moves = []
    board = state.board
    for i, j in enumerate(board):
        for k, l in enumerate(j):
            if l == 0:
                row = [i, k]
                moves.append(row)
    return moves


def result(state, move):
    board = state.board
    to_move = state.to_move
    (m, n) = move

    if to_move == '1':
        mark = 1
        board[m][n] = mark
        board = change_board(board, move, mark)
    elif to_move == '2':
        mark = 2
        board[m][n] = mark
        board = change_board(board, move, mark)

    if to_move == '1':
        to_move = '2'
    else:
        to_move = '1'

    return GameState(to_move=to_move, board=board)


def init_board(board):
    my_emitters = []
    opp_emitters = []
    for i, j in enumerate(board):
        for k, l in enumerate(j):
            if l == 1:
                row = [i, k]
                my_emitters.append(row)
            if l == 2:
                row = [i, k]
                opp_emitters.append(row)

    for place in my_emitters:
        board = change_board(board, place, 1)

    for place in opp_emitters:
        board = change_board(board, place, 2)

    return board


def change_board(board, place, val):
    length = len(board)
    (m, n) = place
    mark = val
    for i in range(1, 4):
        if m - i >= 0:
            if board[m - i][n] == 3:
                break
            if board[m - i][n] == 0:
                board[m - i][n] = mark
            elif board[m - i][n] == mark:
                continue
            else:
                board[m - i][n] = 4

    for i in range(1, 4):
        if m + i < length:
            if board[m + i][n] == 3:
                break
            if board[m + i][n] == 0:
                board[m + i][n] = mark
            elif board[m + i][n] == mark:
                continue
            else:
                board[m + i][n] = 4

    for i in range(1, 4):
        if n - i >= 0:
            if board[m][n - i] == 3:
                break
            if board[m][n - i] == 0:
                board[m][n - i] = mark
            elif board[m][n - i] == mark:
                continue
            else:
                board[m][n - i] = 4

    for i in range(1, 4):
        if n + i < length:
            if board[m][n + i] == 3:
                break
            if board[m][n + i] == 0:
                board[m][n + i] = mark
            elif board[m][n + i] == mark:
                continue
            else:
                board[m][n + i] = 4

    for i in range(1, 4):
        if m + i < length and n + i < length:
            if board[m + i][n + i] == 3:
                break
            if board[m + i][n + i] == 0:
                board[m + i][n + i] = mark
            elif board[m + i][n + i] == mark:
                continue
            else:
                board[m + i][n + i] = 4

    for i in range(1, 4):
        if m - i >= 0 and n - i >= 0:
            if board[m - i][n - i] == 3:
                break
            if board[m - i][n - i] == 0:
                board[m - i][n - i] = mark
            elif board[m - i][n - i] == mark:
                continue
            else:
                board[m - i][n - i] = 4

    for i in range(1, 4):
        if m + i < length and n - i >= 0:
            if board[m + i][n - i] == 3:
                break
            if board[m + i][n - i] == 0:
                board[m + i][n - i] = mark
            elif board[m + i][n - i] == mark:
                continue
            else:
                board[m + i][n - i] = 4

    for i in range(1, 4):
        if m - i >= 0 and n + i < length:
            if board[m - i][n + i] == 3:
                break
            if board[m - i][n + i] == 0:
                board[m - i][n + i] = mark
            elif board[m - i][n + i] == mark:
                continue
            else:
                board[m - i][n + i] = 4

    return board


def utility(state):
    my_score = 0
    opp_score = 0
    board = state.board

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 1:
                my_score += 1
            if board[i][j] == 2:
                opp_score += 1

    return my_score - opp_score


def terminal_test(state):
    if len(actions(state)) == 0:
        return True
    else:
        return False


def alpha_beta_search(state):

    def max_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return utility(state)
        v = -infinity
        for a in actions(state):
            v = max(v, min_value(result(state, a),
                                 alpha, beta, depth + 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return utility(state)
        v = infinity
        for a in actions(state):
            v = min(v, max_value(result(state, a),
                                 alpha, beta, depth + 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    best_score = -infinity
    beta = infinity
    best_action = None
    for a in actions(state):
        temp_state = copy.deepcopy(state)
        v = min_value(result(temp_state, a), best_score, beta, 1)
        if v > best_score:
            best_score = v
            best_action = a
    return best_action


def cutoff_test(state, depth):
    return depth > 5 or terminal_test(state)


def main():
    board = read_file("input0.txt")
    initial_board = init_board(board)
    initial_state = GameState(to_move='1', board=initial_board)
    (i, j) = alpha_beta_search(initial_state)
    my_file = open('output.txt', 'w')
    my_result = str(i) + " " + str(j)
    my_file.write(my_result)


if __name__ == '__main__':
    main()
