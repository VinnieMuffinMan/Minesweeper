import board

if __name__ == "__main__":
    print("Minesweeper")
    size = input("Board size? ")
    m = int(input("Mines? "))
    open = int(input("Guarantee opening? (0/1) "))
    w, h = size.split(",")
    move = input("Move? ")
    x, y = move.split(",")
    b, o = board.search_start(int(x), int(y), int(w), int(h), int(m), open)
    print(board.board_to_string(b))
    move = input("Move? (x to quit) ")
    while move != "x":
        if move[0] == "f":
            move = move[1:]
            x, y = move.split(",")
            o = board.flag(b, int(x), int(y))
        else:
            x, y = move.split(",")
            o = board.search(b, int(x), int(y))
        if o == 1:
            print("BOOM")
            print(board.board_to_string(b, True))
            break
        if o == 2:
            print("Empty")
        if o == 0:
            print(board.board_to_string(b))
        if board.check_win(b):
            print("Winner")
            break
        move = input("Move? (x to quit) ")
