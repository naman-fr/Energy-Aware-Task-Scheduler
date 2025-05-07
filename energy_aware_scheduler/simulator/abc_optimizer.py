import random
import numpy as np

class ArtificialBeeColony:
    def __init__(self, food_sources, max_cycles=100, colony_size=20):
        self.food_sources = food_sources  # List of candidate solutions (tasks)
        self.max_cycles = max_cycles
        self.colony_size = colony_size
        self.num_sources = len(food_sources)
        self.trial_counters = [0] * self.num_sources
        self.fitness = [self.calculate_fitness(fs) for fs in food_sources]
        self.best_source = food_sources[0]
        self.best_fitness = self.fitness[0]

    def calculate_fitness(self, solution):
        # Fitness function: minimize completion time (example)
        return 1.0 / (1.0 + solution['completion_time'])

    def send_employed_bees(self):
        for i in range(self.num_sources):
            k = random.choice([x for x in range(self.num_sources) if x != i])
            phi = random.uniform(-1, 1)
            new_solution = self.modify_solution(self.food_sources[i], self.food_sources[k], phi)
            new_fitness = self.calculate_fitness(new_solution)
            if new_fitness > self.fitness[i]:
                self.food_sources[i] = new_solution
                self.fitness[i] = new_fitness
                self.trial_counters[i] = 0
                if new_fitness > self.best_fitness:
                    self.best_source = new_solution
                    self.best_fitness = new_fitness
            else:
                self.trial_counters[i] += 1

    def modify_solution(self, sol_i, sol_k, phi):
        # Modify solution by adjusting completion time slightly
        new_completion_time = sol_i['completion_time'] + phi * (sol_i['completion_time'] - sol_k['completion_time'])
        new_completion_time = max(0.1, new_completion_time)  # Ensure positive
        new_solution = sol_i.copy()
        new_solution['completion_time'] = new_completion_time
        return new_solution

    def calculate_probabilities(self):
        max_fit = max(self.fitness)
        probs = [0.9 * (f / max_fit) + 0.1 for f in self.fitness]
        return probs

    def send_onlooker_bees(self):
        probs = self.calculate_probabilities()
        i = 0
        t = 0
        while t < self.colony_size:
            if random.random() < probs[i]:
                k = random.choice([x for x in range(self.num_sources) if x != i])
                phi = random.uniform(-1, 1)
                new_solution = self.modify_solution(self.food_sources[i], self.food_sources[k], phi)
                new_fitness = self.calculate_fitness(new_solution)
                if new_fitness > self.fitness[i]:
                    self.food_sources[i] = new_solution
                    self.fitness[i] = new_fitness
                    self.trial_counters[i] = 0
                    if new_fitness > self.best_fitness:
                        self.best_source = new_solution
                        self.best_fitness = new_fitness
                else:
                    self.trial_counters[i] += 1
                t += 1
            i = (i + 1) % self.num_sources

    def send_scout_bees(self):
        limit = 10
        for i in range(self.num_sources):
            if self.trial_counters[i] > limit:
                self.food_sources[i] = self.generate_new_solution()
                self.fitness[i] = self.calculate_fitness(self.food_sources[i])
                self.trial_counters[i] = 0

    def generate_new_solution(self):
        # Generate a new random solution
        return {'completion_time': random.uniform(0.1, 10.0)}

    def optimize(self):
        for cycle in range(self.max_cycles):
            self.send_employed_bees()
            self.send_onlooker_bees()
            self.send_scout_bees()
        return self.best_source
