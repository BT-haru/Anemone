import random

BLACK = 1
WHITE = 2

# 初期の6x6ボード
board = [
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 1, 2, 0, 0],
    [0, 0, 2, 1, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
]

def can_place_x_y(board, stone, x, y):
    if board[y][x] != 0:
        return False

    opponent = 3 - stone
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        found_opponent = False

        while 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == opponent:
            found_opponent = True
            nx += dx
            ny += dy

        if found_opponent and 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == stone:
            return True

    return False

def can_place(board, stone):
    for y in range(len(board)):
        for x in range(len(board[0])):
            if can_place_x_y(board, stone, x, y):
                return True
    return False

def make_move(board, stone, x, y):
    new_board = [row[:] for row in board]
    opponent = 3 - stone
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    new_board[y][x] = stone

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        flips = []

        while 0 <= nx < len(board[0]) and 0 <= ny < len(board) and new_board[ny][nx] == opponent:
            flips.append((nx, ny))
            nx += dx
            ny += dy

        if 0 <= nx < len(board[0]) and 0 <= ny < len(board) and new_board[ny][nx] == stone:
            for fx, fy in flips:
                new_board[fy][fx] = stone

    return new_board

def evaluate_board(board, stone):
    opponent = 3 - stone
    score = 0

    # 重み付けのための評価マップ
    weight_map = [
        [100, -20, 10, 10, -20, 100],
        [-20, -50, -2, -2, -50, -20],
        [10, -2, 1, 1, -2, 10],
        [10, -2, 1, 1, -2, 10],
        [-20, -50, -2, -2, -50, -20],
        [100, -20, 10, 10, -20, 100]
    ]

    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] == stone:
                score += weight_map[y][x]
            elif board[y][x] == opponent:
                score -= weight_map[y][x]

    return score

def minimax(board, stone, depth, is_maximizing):
    opponent = 3 - stone

    if depth == 0 or not can_place(board, stone) and not can_place(board, opponent):
        return evaluate_board(board, stone)

    if is_maximizing:
        max_eval = -float('inf')
        for y in range(len(board)):
            for x in range(len(board[0])):
                if can_place_x_y(board, stone, x, y):
                    new_board = make_move(board, stone, x, y)
                    eval = minimax(new_board, opponent, depth - 1, False)
                    max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for y in range(len(board)):
            for x in range(len(board[0])):
                if can_place_x_y(board, opponent, x, y):
                    new_board = make_move(board, opponent, x, y)
                    eval = minimax(new_board, stone, depth - 1, True)
                    min_eval = min(min_eval, eval)
        return min_eval

def dynamic_depth(empty_cells):
    if empty_cells > 20:
        return 2
    elif empty_cells > 10:
        return 3
    else:
        return 5

def best_place_with_risk_management(board, stone):
    corners = [(0, 0), (0, 5), (5, 0), (5, 5)]
    x_squares = [(0, 1), (1, 0), (1, 1), (0, 4), (1, 5), (1, 4),
                 (4, 0), (5, 1), (4, 1), (4, 5), (5, 4), (4, 4)]

    best_score = -float('inf')
    best_move = None

    for y in range(len(board)):
        for x in range(len(board[0])):
            if not can_place_x_y(board, stone, x, y):
                continue

            if (x, y) in corners:
                return (x, y)

            score = evaluate_board(make_move(board, stone, x, y), stone)

            if (x, y) in x_squares:
                score -= 100

            if score > best_score:
                best_score = score
                best_move = (x, y)

    return best_move

class AnemoneAI(object):

    def face(self):
        return "🌺"

    def place(self, board, stone):
        empty_cells = sum(row.count(0) for row in board)
        depth = dynamic_depth(empty_cells)

        best_eval = -float('inf')
        best_move = None

        for y in range(len(board)):
            for x in range(len(board[0])):
                if can_place_x_y(board, stone, x, y):
                    new_board = make_move(board, stone, x, y)
                    eval = minimax(new_board, stone, depth, False)
                    if eval > best_eval:
                        best_eval = eval
                        best_move = (x, y)

       # if best_move is None:
        #    return None  # 打てる手がない場合

        #return best_move
