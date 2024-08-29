import random


def start(w: int, h: int, m: int):
    board = [[-1 for __ in range(w)] for _ in range(h)]
    while m > 0:
        ran = random.randint(0, w * h - 1)
        if board[ran // w][ran % w] == -2:
            continue
        board[ran // w][ran % w] = -2
        m -= 1
    return board


def search_start(x: int, y: int, w: int, h: int, m: int, opening=False):
    board = start(w, h, m)
    valid = False
    while not valid:
        valid = True
        if board[y][x] == -2:
            board = start(w, h, m)
            valid = False
            continue
        if opening:
            adj = get_adj(board, x, y)
            for a, b in adj:
                if board[b][a] == -2:
                    board = start(w, h, m)
                    valid = False
                    break

    return (board, search(board, x, y))


def search(board, x: int, y: int):
    if board[y][x] == -2:
        return 1
    if board[y][x] == 0 or board[y][x] == -3:
        return 2
    if board[y][x] > 0:
        return number_click(board, x, y)
    search = [(x, y)]
    _search(board, search)
    return 0


def get_adj(board, x: int, y: int):
    w = len(board[0])
    h = len(board)
    if x == 0:
        if y == 0:
            return [(1, 0), (0, 1), (1, 1)]
        if y == h - 1:
            return [(0, y - 1), (1, y - 1), (1, y)]
        return [(0, y - 1), (1, y - 1), (1, y), (0, y + 1), (1, y + 1)]
    if x == w - 1:
        if y == 0:
            return [(x - 1, 0), (x - 1, 1), (x, 1)]
        if y == h - 1:
            return [(x - 1, y - 1), (x, y - 1), (x - 1, y)]
        return [(x - 1, y - 1), (x, y - 1), (x - 1, y), (x - 1, y + 1), (x, y + 1)]
    if y == 0:
        return [(x - 1, 0), (x + 1, 0), (x - 1, 1), (x, 1), (x + 1, 1)]
    if y == h - 1:
        return [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1), (x - 1, y), (x + 1, y)]
    return [
        (x - 1, y - 1),
        (x, y - 1),
        (x + 1, y - 1),
        (x - 1, y),
        (x + 1, y),
        (x - 1, y + 1),
        (x, y + 1),
        (x + 1, y + 1),
    ]


def pretty_to_string(board, mines=False):
    w = len(board[0]) - 1
    h = len(board) - 1
    s = ""
    for i in range(len(str(w)) - 1, -1, -1):
        s += " " * (len(str(h)) + 1)
        c = 0
        d = 10**i
        first_zero = i > 0
        for i in range(w + 1):
            if first_zero:
                s += " "
            else:
                s += str(c)
            if i % d == d - 1:
                c += 1
                c %= 10
                first_zero = False
        s += "\n"

    s += "\n"
    if mines:
        dic = {-4: "F", -3: "f", -2: "X", -1: "."}
    else:
        dic = {-4: "f", -3: "f", -2: ".", -1: "."}

    for i, row in enumerate(board):
        num = ("%" + str(len(str(h))) + "d ") % i
        s += num
        for col in row:
            if col < 0:
                s += dic[col]
            else:
                s += str(col)
        s += "\n"
    return s


def board_to_string(board, mines=False):
    s = ""
    if mines:
        dic = {-4: "F", -3: "f", -2: "X", -1: "."}
    else:
        dic = {-4: "f", -3: "f", -2: ".", -1: "."}

    for row in board:
        for col in row:
            if col < 0:
                s += dic[col]
            else:
                s += str(col)
        s += "\n"
    return s


def flag(board, x: int, y: int):
    if board[y][x] == -1 or board[y][x] == -2:
        board[y][x] -= 2
        return 0
    if board[y][x] == -3 or board[y][x] == -4:
        board[y][x] += 2
        return 0
    return 2


def number_click(board, x: int, y: int):
    flags = 0
    adj = get_adj(board, x, y)
    for a, b in adj:
        if board[b][a] < -2:
            flags += 1
    if flags != board[y][x]:
        return 2
    search = []
    for a, b in adj:
        if board[b][a] == -2:
            return 1
        if board[b][a] == -1:
            search.append((a, b))
    _search(board, search)
    return 0


def _search(board, search):
    while len(search) > 0:
        a, b = search.pop()
        if board[b][a] != -1:
            continue
        mines = 0
        adj = get_adj(board, a, b)
        for c, d in adj:
            if board[d][c] == -2 or board[d][c] == -4:
                mines += 1
        board[b][a] = mines
        if mines == 0:
            search.extend(adj)


def check_win(board):
    for row in board:
        for col in row:
            if col == -4:
                return False
            if col == -2:
                return False
    return True


if __name__ == "__main__":
    ans = input()
    board, a = search_start(int(ans[0]), int(ans[1]), 5, 5, 10)
    print(a)
    print(board_to_string(board))

    while ans != "X":
        ans = input()
        print(search(board, int(ans[0]), int(ans[1])))
        print(board_to_string(board))
