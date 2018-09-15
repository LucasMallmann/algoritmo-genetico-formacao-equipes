from app_api.genetic_algorithm.dna import Dna
import numpy as np


class Population(object):
    def __init__(self, total_population: int):
        self.total_population = total_population
        self.population = []

    def generate_initial_population(self, total_of_groups: int, persons_by_group: int):
        self.PARAMS = np.random.random_integers(
            1, 5, (3, total_of_groups * persons_by_group))
        
        # self.PARAMS = [
        #     [1, 2, 1, 3, 1, 4],
        #     [2, 2, 1, 4, 4, 1],
        #     [1, 1, 3, 1, 1, 1]
        # ]

        print('*' * 120)
        print(self.PARAMS)
        print('*' * 120)


        for i in range(self.total_population):
            dna = Dna(total_of_groups, persons_by_group)
            self.population.append(dna)

    def calc_fitness(self):
        for individual in self.population:
            individual.calc_fitness()
