import functions
import random

def fit(n, child_count = 10, mutation_prob = 0.1, generations = 100):
    boards = [functions.generateBoard(n) for _ in range(child_count)]
    max_fitness = n * (n - 1) // 2
    
    for i in range(generations):
        new_boards = []
        for j in range(child_count):
            x = functions.select_parent(boards)
            y = functions.select_parent(boards)
            while x == y:
                y = functions.select_parent(boards)
            child = functions.crossover(x, y)
            if mutation_prob > random.random():
                child = functions.mutate(child)
                
            new_boards.append(child)
            
        boards = new_boards
        highest_score = boards[0]
        for board in boards:
            if functions.fitness(board) > functions.fitness(highest_score):
                highest_score = board
        
        functions.printBoard(highest_score)
        
        print("Generation: ", i, "Fitness: ", functions.fitness(highest_score))
        
        if functions.fitness(highest_score) == max_fitness:
            print("Solution found!")
            break
            
    
    

if __name__ == "__main__":
    fit(8, child_count=20, mutation_prob=0.1, generations=1000)