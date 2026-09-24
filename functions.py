def checkConflicts(board): # count all conflicts in a board
    n = len(board)
    conflicts = 0
    
    # check duplicates numbers in board
    #  2 3 4 2 2

    # "3": 1
    # "2": 3
    # "4": 1

    if len(board) != len(set(board)):
        # check duplicate count
        conflicts += (len(board) - len(set(board))) + 1

    # check all diagonals
    diag1 = set()  # row - col
    diag2 = set()  # row + col

    for row, col in enumerate(board):
        if row - col in diag1:
            conflicts += 1
        else:
            diag1.add(row - col)

        if row + col in diag2:
            conflicts += 1
        else:
            diag2.add(row + col)


    return conflicts


def next_column(board, row):
    return board[row].index(1)


def move(queens, board, row=0):
    if row == queens:
        return True

    for col in range(queens):
        if is_safe(board, row, col):
            board[row][col] = 1

            if move(queens, board, row + 1):
                return True

            # This choice failed; clear it and try the next column.
            board[row][col] = 0

    return False


def fitness(board):
    queens = len(board)
    conflicts = 0

    