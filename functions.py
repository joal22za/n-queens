def is_safe(board, row, col):
    # A queen must not share a column with an earlier queen.
    for previous_row in range(row):
        if board[previous_row][col] == 1:
            return False

    # Only earlier rows need checking because later rows are still empty.
    for previous_row in range(row):
        column_difference = abs(col - next_column(board, previous_row))
        if column_difference == row - previous_row:
            return False

    return True


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