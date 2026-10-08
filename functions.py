import random 

def checkConflicts(board):
    n = len(board)
    conflicts = 0
    
    rows = {}
    for row_val in board:
        if row_val not in rows:
            rows[row_val] = 1
        else:
            rows[row_val] += 1

    for count in rows.values():
        conflicts += count * (count - 1) // 2

    diag1 = {} 
    diag2 = {} 

    for row, col in enumerate(board):
        if row - col in diag1:
            diag1[row - col] += 1
        else:
            diag1[row - col] = 1
            
        if row + col in diag2:
            diag2[row + col] += 1
        else:
            diag2[row + col] = 1
            
    for count in diag1.values():
        conflicts += count * (count - 1) // 2

    for count in diag2.values():
        conflicts += count * (count - 1) // 2

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
            if board[col] == row:
                line += "Q "
            else:
                line += ". "
        print(line)
    print()  

def fitness(board):
    n = len(board)
    max_conflicts = n * (n - 1) // 2
    return max_conflicts - checkConflicts(board)

# 3 tournament selection
def select_parent(boards):
    
    candidates = random.sample(boards, 3)
    b = candidates[0]

    if fitness(candidates[1]) > fitness(b):
        b = candidates[1]

    if fitness(candidates[2]) > fitness(b):
        b = candidates[2]

    return b

def crossover(parent1, parent2):
    n = len(parent1)
    crossover_point = random.randint(1, n - 1)

    child1 = parent1[:crossover_point] + parent2[crossover_point:]

    return child1
