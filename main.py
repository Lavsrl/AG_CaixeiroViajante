import random

mutation_rate = 0.1

def generate_random_distances(num_cities, min_distance=10, max_distance=100):
    cities = [chr(65 + i) for i in range(num_cities)]  
    distances = {city: {} for city in cities}

    for i, city1 in enumerate(cities):
        for j, city2 in enumerate(cities):
            if i == j:
                distances[city1][city2] = 0
            elif city2 not in distances[city1]:
                dist = random.randint(min_distance, max_distance)
                distances[city1][city2] = dist
                distances[city2][city1] = dist

    return distances, cities

num_cities = 15 
distances, cities = generate_random_distances(num_cities)

class Individual: 
    def __init__(self, genes=None):
        self.genes = genes if genes else random.sample(cities, len(cities))
        self.fitness = self.evaluate_fitness() 

    def evaluate_fitness(self): # distancia total
        total_distance = 0 
        for i in range(len(self.genes) - 1):
            total_distance += distances[self.genes[i]][self.genes[i+1]]
        total_distance += distances[self.genes[-1]][self.genes[0]] 
        return total_distance 

    @staticmethod 
    def crossover(parent1, parent2):
        size = len(parent1.genes)
        start, end = sorted(random.sample(range(size), 2))  
        child_genes = [None] * size  
        child_genes[start:end] = parent1.genes[start:end] # pai 1

        remaining_cities = [city for city in parent2.genes if city not in child_genes] # restante pai 2
        for i in range(size): 
            if child_genes[i] is None: 
                child_genes[i] = remaining_cities.pop(0)

        print(f"Crossover entre {parent1.genes} e {parent2.genes} -> Filho: {child_genes}")
        return Individual(child_genes)

    def mutate(self, mutation_rate=0.3): 
        if random.random() < mutation_rate:
            idx1, idx2 = random.sample(range(len(self.genes)), 2)
            print(f"Mutacao antes: {self.genes}")
            print(f"Trocando {self.genes[idx1]} com {self.genes[idx2]}")  
            self.genes[idx1], self.genes[idx2] = self.genes[idx2], self.genes[idx1]
            print(f"Mutacao depois: {self.genes}")
        self.fitness = self.evaluate_fitness()


def genetic_algorithm(pop_size=20, generations=2, mutation_rate=0.3): 
    population = [Individual() for _ in range(pop_size)] 

    print("\n Populacaoo inicial:")
    for i, ind in enumerate(population): 
        print(f"Individuo {i}: {ind.genes} -> Distancia: {ind.fitness}")

    for gen in range(generations): 
        best_individual = min(population, key=lambda ind: ind.fitness) 
        print(f"\n Geracao {gen + 1} - Melhor ate agora: {best_individual.genes} ({best_individual.fitness})")

        new_population = population[:3]  

        while len(new_population) < pop_size: 
            p1, p2 = random.sample(population[:5], 2)  # cinco melhores para crossover
            p1.mutate(mutation_rate)
            p2.mutate(mutation_rate)

            child = Individual.crossover(p1, p2) 
            new_population.append(child) # adiciona o filho na populacao

        population = new_population

    best = min(population, key=lambda ind: ind.fitness) 
    return best

best_solution = genetic_algorithm()
print("\n Melhor solucao encontrada:", best_solution.genes) 
print("Distancia total:", best_solution.fitness)
