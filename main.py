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
        if i % 20 == 0:
            print("Generation: ", i, "Fitness: ", functions.fitness(highest_score), " Conflicts: ", functions.checkConflicts(highest_score))
        
        if functions.fitness(highest_score) == max_fitness:
            functions.printBoard(highest_score)
            print("Solution found! in generation: ", i)
            break

def paramter_tuning(parameter_grid):

if __name__ == "__main__":
    for n in [4, 8, 12, 16]:
        print(f"Testing n = {n}...")
        results = [run_experiment(n) for _ in range(5)] # Kör 5 gånger per n för medelvärde
        
        successful_runs = [r for r in results if r["success"]]
        success_rate = (len(successful_runs) / len(results)) * 100
        avg_gen = sum(r["generations"] for r in successful_runs) / len(successful_runs) if successful_runs else "N/A"
        avg_time = sum(r["time"] for r in successful_runs) / len(successful_runs) if successful_runs else "N/A"
        
        print(f"Result for n={n}: Success Rate: {success_rate}%, Avg Generations: {avg_gen}, Avg Time: {avg_time:.4f}s\n")