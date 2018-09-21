from app_api.genetic_algorithm.dna import Dna
import numpy as np
import random


def generate_parameters(total_of_persons):
    return np.random.random_integers(
        1, 5, (3, total_of_persons))


class Population(object):
    def __init__(self, total_population: int, mutation_rate):
        self.total_population = total_population
        self.population = []
        self.mutation_rate = mutation_rate
        self.generations = 0

    def generate_initial_population(self, total_of_groups: int, persons_by_group: int):
        self.PARAMETERS = np.random.random_integers(
            1, 5, (3, total_of_groups * persons_by_group))

        print('*' * 120)
        print(self.PARAMETERS)
        print('*' * 120)

        for i in range(self.total_population):
            dna = Dna(total_of_groups, persons_by_group)
            self.population.append(dna)

    def calc_fitness(self):
        for individual in self.population:
            individual.calc_fitness(self.PARAMETERS)

    def generate(self) -> list:
        '''
        Gerar uma nova população a partir dos cruzamentos
        '''
        for i, ind in enumerate(self.population):
            print('--------------------------GENERATION--------------------------------------')
            parent1 = self.select_one_parent()
            parent2 = self.select_one_parent()
            print('PARENTS')
            print(parent1)
            print(parent2)
            child = parent1.crossover(parent2)
            child.calc_fitness(self.PARAMETERS)
            print('CHILD = %s' %child)
            self.population[i] = child
            print('--------------------------END GENERATION--------------------------------------')
        self.generations += 1
        return self.population

    def select_one_parent(self) -> Dna:
        """
        Irá selecionar um indivíduo para ser o pai
        """
        total = sum([individual.fitness for individual in self.population])
        pick = random.uniform(0, total)
        current = 0
        for i, individual in enumerate(self.population):
            current += individual.fitness
            if current > pick:
                print('CHOOSEN PARENT INDEX ', i)
                return individual
