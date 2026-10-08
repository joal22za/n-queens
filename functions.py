import random 
import time

def fit(n, child_count = 10, mutation_prob = 0.1, generations = 1000):
    start_time = time.time()
    boards = [generateBoard(n) for _ in range(child_count)]
    max_fitness = n * (n - 1) // 2
    
    for i in range(generations):
        new_boards = []
        for j in range(child_count):
            x = select_parent(boards)
            y = select_parent(boards)
            attempt = 0
            while x == y and attempt < 10:
                y = select_parent(boards)
                attempt += 1

            child = crossover(x, y)
            if mutation_prob > random.random():
                child = mutate(child)
                
            new_boards.append(child)
            
        boards = new_boards
        highest_score = boards[0]
        for board in boards:
            if fitness(board) > fitness(highest_score):
                highest_score = board
        
        conflicts = max_fitness - fitness(highest_score)
        
        # Enkel och ren utskrift: Start, var 500:e eller noll
        if i == 0 or i % 500 == 0 or conflicts == 0: 
            print(f"[Standard] ({i},{conflicts})")
        
        if fitness(highest_score) == max_fitness:
            elapsed_time = time.time() - start_time
            return {
                "success": True,
                "generations": i,
                "time": elapsed_time
            }
            
    elapsed_time = time.time() - start_time
    return {
        "success": False,
        "generations": generations,
        "time": elapsed_time
    }

def fit_mutation_only(n, child_count=10, mutation_prob=0.2, generations=1000):
    start_time = time.time()
    boards = [generateBoard(n) for _ in range(child_count)]
    max_fitness = n * (n - 1) // 2
    
    for i in range(generations):
        new_boards = []
        for j in range(child_count):
            parent = select_parent(boards)
            child = list(parent)
            if mutation_prob > random.random():
                child = mutate(child)
                
            new_boards.append(child)
            
        boards = new_boards
        highest_score = boards[0]
        for board in boards:
            if fitness(board) > fitness(highest_score):
                highest_score = board
        
        conflicts = max_fitness - fitness(highest_score)
        
        if i == 0 or i % 500 == 0 or conflicts == 0:
            print(f"[Mutation Only] ({i},{conflicts})")
            
        if fitness(highest_score) == max_fitness:
            elapsed_time = time.time() - start_time
            return {
                "success": True,
                "generations": i,
                "time": elapsed_time
            }
            
    elapsed_time = time.time() - start_time
    return {
        "success": False,
        "generations": generations,
        "time": elapsed_time
    }

def get_conflicting_columns(board):
    n = len(board)
    conflicting_cols = set()
    for i in range(n):
        for j in range(i + 1, n):
            if board[i] == board[j] or abs(i - j) == abs(board[i] - board[j]):
                conflicting_cols.add(i)
                conflicting_cols.add(j)
    return list(conflicting_cols)

def adaptive_target_probability(initial_conflicts, current_conflicts):
    if initial_conflicts == 0:
        return 1.0
    return max(0.0, min(1.0, 1.0 - current_conflicts / initial_conflicts)) # probability of mutation based on conflicts, increases as conflicts decrease


def fit_adaptive_mutation(n, child_count=20, generations=3000, elite_count=1):
    if child_count < 3:
        print("Tournament selection requires at least three boards")
        return 1
    if not 1 <= elite_count < child_count:
        print("must preserve at least one board and leave room for offspring")
        return 1

    start_time = time.time()
    boards = [generateBoard(n) for _ in range(child_count)]
    max_fitness = n * (n - 1) // 2
    initial_best = max(boards, key=fitness)
    initial_conflicts = max_fitness - fitness(initial_best)
    
    for i in range(generations):
        ranked_boards = sorted(boards, key=fitness, reverse=True) # bästa brädan först på listan
        current_conflicts = max_fitness - fitness(ranked_boards[0]) 
        conflict_prob = adaptive_target_probability(initial_conflicts, current_conflicts) #gör så att fokuserade mutationer sker mer mot slutet.
            
        new_boards = [list(board) for board in ranked_boards[:elite_count]]
        for offspring_index in range(child_count - elite_count):
            parent = ranked_boards[0] if offspring_index == 0 else select_parent(boards)
            child = list(parent)
            
            if conflict_prob > 0 and random.random() < conflict_prob:
                conflicts = get_conflicting_columns(child)
                if conflicts:
                    col = random.choice(conflicts)
                    child[col] = random.randint(0, n - 1)
                else:
                    child = mutate(child)
            else:
                child = mutate(child)
                
            new_boards.append(child)
            
        boards = new_boards
        highest_score = max(boards, key=fitness)
        
        conflicts = max_fitness - fitness(highest_score)
        
        if i == 0 or i % 500 == 0 or conflicts == 0:        
            print(f"[Adaptive] ({i},{conflicts})")

        if fitness(highest_score) == max_fitness:
            elapsed_time = time.time() - start_time
            return {
                "success": True,
                "generations": i,
                "time": elapsed_time
            }
            
    elapsed_time = time.time() - start_time
    return {
        "success": False,
        "generations": generations,
        "time": elapsed_time
    }


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
