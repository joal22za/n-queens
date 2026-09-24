import random 

def checkConflicts(board): # count all conflicts in a board
    n = len(board)
    conflicts = 0
    
    # check duplicates numbers in board
    #  2 3 4 2 2

    # "3": 1
    # "2": 3
    # "4": 1

    columns = {}

    for col in board:
        if col not in columns:
            columns[col] = 1
        else:
            columns[col] += 1

    for count in columns.values():
        conflicts += count * (count - 1) // 2

    # check all diagonals
    diag1 = set()  # row - col
    diag2 = set()  # row + col

    for row, col in enumerate(board):
        if row - col in diag1: # checks the diagonal from top-left to bottom-right
            conflicts += 1
        else:
            diag1.add(row - col)

        if row + col in diag2: # check the diagonal from top-right to bottomleft
            conflicts += 1
        else:
            diag2.add(row + col)


    return conflicts

def generateBoard(n):
    import random
    return [random.randint(0, n - 1) for _ in range(n)]

def mutate(board):
    child = list(board)
    index = random.randint(0, len(board) - 1)
    child[index] = random.randint(0, len(board) - 1)
    return child

def printBoard(board):
    n = len(board)
    for row in range(n):
        line = ""
        for col in range(n):
            if board[row] == col:
                line += "Q "
            else:
                line += ". "
        print(line)
    return False

def fitness(board):
    n = len(board)
    max_conflicts = n * (n - 1) // 2
    return max_conflicts - checkConflicts(board)

def select_parent(boards):
    a = random.choice(boards)
    b = random.choice(boards)
    
    if(fitness(a) > fitness(b)):
        return a

    return b

def crossover(parent1, parent2):

    n = len(parent1)
    crossover_point = random.randint(1, n - 1)
    
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    
    return child1, child2