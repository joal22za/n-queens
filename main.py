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

        #if i % 100 == 0:
        #    print("Generation: ", i, "Fitness: ", functions.fitness(highest_score), " Conflicts: ", functions.checkConflicts(highest_score))
        
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
            # Välj endast EN förälder (ingen crossover behövs)
            parent = functions.select_parent(boards)
            
            # Skapa en kopia och mutera direkt
            child = list(parent)
            if mutation_prob > random.random():
                child = functions.mutate(child)
                
            new_boards.append(child)
            
        boards = new_boards
        highest_score = boards[0]
        for board in boards:
            if functions.fitness(board) > functions.fitness(highest_score):
                highest_score = board
                
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
    """Hjälpfunktion som identifierar vilka kolumner (drottningar) som är i konflikt."""
    n = len(board)
    conflicting_cols = set()
    for i in range(n):
        for j in range(i + 1, n):
            # Samma rad eller samma diagonal
            if board[i] == board[j] or abs(i - j) == abs(board[i] - board[j]):
                conflicting_cols.add(i)
                conflicting_cols.add(j)
    return list(conflicting_cols)

def fit_adaptive_mutation(n, child_count=20, generations=3000):
    start_time = time.time()
    boards = [functions.generateBoard(n) for _ in range(child_count)]
    max_fitness = n * (n - 1) // 2
    
    for i in range(generations):
        # Gradvis trappstegsschema (Annealing schedule) baserat på generation
        if i < 100:
            conflict_prob = 0.0  # 100% slump (Ren utforskning i början)
        elif i < 500:
            conflict_prob = 0.2  # 80% slump / 20% målstyrd
        elif i < 1500:
            conflict_prob = 0.5  # 50% slump / 50% målstyrd
        elif i < 2500:
            conflict_prob = 0.8  # 20% slump / 80% målstyrd (Finslipning)
        else:
            conflict_prob = 1.0  # 100% målstyrd reparation på slutet
            
        new_boards = []
        for _ in range(child_count):
            parent = functions.select_parent(boards)
            child = list(parent)
            
            # Välj mellan målstyrd reparation eller slumpmässig mutation
            if conflict_prob > 0 and random.random() < conflict_prob:
                conflicts = get_conflicting_columns(child)
                if conflicts:
                    # Välj en drottning som faktiskt bråkar och flytta den till en ny rad
                    col = random.choice(conflicts)
                    child[col] = random.randint(0, n - 1)
                else:
                    child = functions.mutate(child)
            else:
                # Ren slumpmässig mutation (utforskning)
                child = functions.mutate(child)
                
            new_boards.append(child)
            
        boards = new_boards
        
        # Hitta bästa brädet i populationen
        highest_score = max(boards, key=functions.fitness)
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
    for n in [4, 8, 12, 16]:
        print(f"=== Testing n = {n} ===")
        
        # 1. Vanlig algoritm (med crossover)
        results_normal = [fit(n, child_count=20, mutation_prob=0.1, generations=5000) for _ in range(5)]
        succ_normal = [r for r in results_normal if r["success"]]
        rate_normal = (len(succ_normal) / len(results_normal)) * 100
        gen_normal = sum(r["generations"] for r in succ_normal) / len(succ_normal) if succ_normal else "N/A"
        time_normal = sum(r["time"] for r in succ_normal) / len(succ_normal) if succ_normal else "N/A"
        
        print(f"  [Standard EA]  Success: {rate_normal}%, Gen: {gen_normal}, Time: {time_normal if isinstance(time_normal, str) else f'{time_normal:.4f}s'}")
        
        # 2. Endast mutation (enklare variant för jämförelse)
        results_mutation = [fit_mutation_only(n, child_count=20, mutation_prob=0.2, generations=5000) for _ in range(5)]
        succ_mut = [r for r in results_mutation if r["success"]]
        rate_mut = (len(succ_mut) / len(results_mutation)) * 100
        gen_mut = sum(r["generations"] for r in succ_mut) / len(succ_mut) if succ_mut else "N/A"
        time_mut = sum(r["time"] for r in succ_mut) / len(succ_mut) if succ_mut else "N/A"
        
        print(f"  [Mutation-only] Success: {rate_mut}%, Gen: {gen_mut}, Time: {time_mut if isinstance(time_mut, str) else f'{time_mut:.4f}s'}\n")
        
        print(f"=== Testing n = {n} with Adaptive Mutation ===")
        
        # Kör den adaptiva strategin 5 gånger för att få ett medelvärde
        results = [fit_adaptive_mutation(n, child_count=20, generations=3000) for _ in range(5)]
        
        successful_runs = [r for r in results if r["success"]]
        success_rate = (len(successful_runs) / len(results)) * 100
        avg_gen = sum(r["generations"] for r in successful_runs) / len(successful_runs) if successful_runs else "N/A"
        avg_time = sum(r["time"] for r in successful_runs) / len(successful_runs) if successful_runs else "N/A"
        
        print(f"Result for n={n}: Success Rate: {success_rate}%, Avg Generations: {avg_gen}, Avg Time: {avg_time if isinstance(avg_time, str) else f'{avg_time:.4f}s'}\n")