# Alexander Johansson, Matti Al hanota

import functions
import random
import time

def fit(n, child_count = 10, mutation_prob = 0.1, generations = 1000):
    start_time = time.time()
    boards = [functions.generateBoard(n) for _ in range(child_count)]
    max_fitness = n * (n - 1) // 2
    
    for i in range(generations):
        new_boards = []
        for j in range(child_count):
            x = functions.select_parent(boards)
            y = functions.select_parent(boards)
            attempt = 0
            while x == y and attempt < 10:
                y = functions.select_parent(boards)
                attempt += 1

            child = functions.crossover(x, y)
            if mutation_prob > random.random():
                child = functions.mutate(child)
                
            new_boards.append(child)
            
        boards = new_boards
        highest_score = boards[0]
        for board in boards:
            if functions.fitness(board) > functions.fitness(highest_score):
                highest_score = board
        
        conflicts = max_fitness - functions.fitness(highest_score)
        
        # Enkel och ren utskrift: Start, var 500:e eller noll
        if i == 0 or i % 500 == 0 or conflicts == 0: 
            print(f"[Standard] ({i},{conflicts})")
        
        if functions.fitness(highest_score) == max_fitness:
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
    boards = [functions.generateBoard(n) for _ in range(child_count)]
    max_fitness = n * (n - 1) // 2
    
    for i in range(generations):
        new_boards = []
        for j in range(child_count):
            parent = functions.select_parent(boards)
            child = list(parent)
            if mutation_prob > random.random():
                child = functions.mutate(child)
                
            new_boards.append(child)
            
        boards = new_boards
        highest_score = boards[0]
        for board in boards:
            if functions.fitness(board) > functions.fitness(highest_score):
                highest_score = board
        
        conflicts = max_fitness - functions.fitness(highest_score)
        
        if i == 0 or i % 500 == 0 or conflicts == 0:
            print(f"[Mutation Only] ({i},{conflicts})")
            
        if functions.fitness(highest_score) == max_fitness:
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
    boards = [functions.generateBoard(n) for _ in range(child_count)]
    max_fitness = n * (n - 1) // 2
    initial_best = max(boards, key=functions.fitness)
    initial_conflicts = max_fitness - functions.fitness(initial_best)
    
    for i in range(generations):
        ranked_boards = sorted(boards, key=functions.fitness, reverse=True) # bästa brädan först på listan
        current_conflicts = max_fitness - functions.fitness(ranked_boards[0]) 
        conflict_prob = adaptive_target_probability(initial_conflicts, current_conflicts) #gör så att fokuserade mutationer sker mer mot slutet.
            
        new_boards = [list(board) for board in ranked_boards[:elite_count]]
        for offspring_index in range(child_count - elite_count):
            parent = ranked_boards[0] if offspring_index == 0 else functions.select_parent(boards)
            child = list(parent)
            
            if conflict_prob > 0 and random.random() < conflict_prob:
                conflicts = get_conflicting_columns(child)
                if conflicts:
                    col = random.choice(conflicts)
                    child[col] = random.randint(0, n - 1)
                else:
                    child = functions.mutate(child)
            else:
                child = functions.mutate(child)
                
            new_boards.append(child)
            
        boards = new_boards
        highest_score = max(boards, key=functions.fitness)
        
        conflicts = max_fitness - functions.fitness(highest_score)
        
        if i == 0 or i % 500 == 0 or conflicts == 0:        
            print(f"[Adaptive] ({i},{conflicts})")

        if functions.fitness(highest_score) == max_fitness:
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

if __name__ == "__main__":
    n = 40
    print(f"=== Testing n = {n} ===")
    
    results_normal = [fit(n, child_count=20, mutation_prob=0.1, generations=5000) for _ in range(5)]
    succ_normal = [r for r in results_normal if r["success"]]
    rate_normal = (len(succ_normal) / len(results_normal)) * 100
    gen_normal = sum(r["generations"] for r in succ_normal) / len(succ_normal) if succ_normal else "N/A"
    time_normal = sum(r["time"] for r in succ_normal) / len(succ_normal) if succ_normal else "N/A"
    print(f"  [Standard EA]  Success: {rate_normal}%, Gen: {gen_normal}, Time: {time_normal if isinstance(time_normal, str) else f'{time_normal:.4f}s'}")
    
    results_mutation = [fit_mutation_only(n, child_count=20, mutation_prob=0.2, generations=5000) for _ in range(5)]
    succ_mut = [r for r in results_mutation if r["success"]]
    rate_mut = (len(succ_mut) / len(results_mutation)) * 100
    gen_mut = sum(r["generations"] for r in succ_mut) / len(succ_mut) if succ_mut else "N/A"
    time_mut = sum(r["time"] for r in succ_mut) / len(succ_mut) if succ_mut else "N/A"
    print(f"  [Mutation-only] Success: {rate_mut}%, Gen: {gen_mut}, Time: {time_mut if isinstance(time_mut, str) else f'{time_mut:.4f}s'}")
        
    results = [fit_adaptive_mutation(n, child_count=20, generations=3000) for _ in range(5)]
    successful_runs = [r for r in results if r["success"]]
    success_rate = (len(successful_runs) / len(results)) * 100
    avg_gen = sum(r["generations"] for r in successful_runs) / len(successful_runs) if successful_runs else "N/A"
    avg_time = sum(r["time"] for r in successful_runs) / len(successful_runs) if successful_runs else "N/A"
    print(f"  [Adaptive-mutation] Success: {success_rate}%, Gen: {avg_gen}, Time: {avg_time if isinstance(avg_time, str) else f'{avg_time:.4f}s'}\n")
