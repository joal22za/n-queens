import functions as p
from functions import move

while True:
    queens = input("")
    if queens.isdigit():
        queens = int(queens)
        break
    else:
        print("Please enter a valid number of queens.")
    
first_row = [1 for i in range(queens)] 
rest_of_matrix = [[0 for i in range(queens)] for i in range(queens - 1)]
board = [first_row] + rest_of_matrix
points = queens



while True:
    if queens <= 3:
        print("There is no solution for a board with less than 4 queens.")  
        break
    else:
        
            
print(board)    


