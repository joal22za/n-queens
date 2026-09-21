import functions as p

while True:
    # Get the number of queens from the user
    queens = input("Input the number of queens: ")
    if queens.isdigit():
        queens = int(queens)
    else:
        print("Please enter a valid number of queens.")
        continue
    
    # Check if the number of queens is less than 4 
    if queens <= 3:
        print("There is no solution for a board with less than 4 queens.")  
        continue
    
    # Start with an empty board and place one queen in each row.
    board = [[0 for _ in range(queens)] for _ in range(queens)]

    if p.move(queens, board):
        for row in board:
            print(" ".join(str(cell) for cell in row))
    else:
        print("No solution found.")

        


