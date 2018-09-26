from app_api.genetic_algorithm.dna import Dna
import numpy as np
import random


def generate_parameters(total_of_persons):
    return np.random.random_integers(
        1, 5, (3, total_of_persons))


def crossover():
    pass


class Population(object):
    def __init__(self, total_population: int,
                 mutation_rate: float,
                 crossover_rate: float):
        self.total_population = total_population
        self.population = []
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.generations = 0

    def generate_initial_population(self, total_of_groups: int, persons_by_group: int):
        self.PARAMETERS = np.random.random_integers(
            1, 5, (3, total_of_groups * persons_by_group))

        self.total_of_groups = total_of_groups
        self.persons_by_group = persons_by_group

        for i in range(self.total_population):
            dna = Dna(total_of_groups, persons_by_group)
            self.population.append(dna)

    def calc_fitness(self):
        for individual in self.population:
            individual.calc_fitness(self.PARAMETERS)

    def crossover(self, dna1: Dna, dna2: Dna, split_position: int):
        child1 = Dna(self.total_of_groups, self.persons_by_group)
        child2 = Dna(self.total_of_groups, self.persons_by_group)
        child1.genes = dna1.genes[:split_position] + \
            dna2.genes[split_position:]
        child2.genes = dna2.genes[:split_position] + \
            dna1.genes[split_position:]

        return child1, child2

    def generate(self) -> list:
        '''
        Irá gerar os descendentes da população.
        Esses descendentes serão escolhidos para formarem uma nova população
        '''

        desc = []

        amount_crossing = round(
            self.total_population * self.crossover_rate
        )  # quantidade de cruzamentos
        
        total_persons = self.persons_by_group * self.total_of_groups
        split_random_position = np.random.randint(1, total_persons)
        print(split_random_position)

        # a quantidade de filhos deve ser 2x a quantidade de cruzamentos
        for i in range(amount_crossing):
            parent1 = self.select_one_parent()
            parent2 = self.select_one_parent()

            print('Parent1 -> %s' % parent1)
            print('Parent2 -> %s' % parent2)

            childs = self.crossover(parent1, parent2, split_random_position)
            child1 = childs[0]
            child2 = childs[1]

            print('child1 = %s ' % child1)
            print('child2 = %s ' % child2)

            # Realizar a mutação
            child1.mutate(self.mutation_rate)
            child2.mutate(self.mutation_rate)
            # Calcular o fitness
            child1.calc_fitness(self.PARAMETERS)
            child2.calc_fitness(self.PARAMETERS)

            desc.append(child1)
            desc.append(child2)
            print('\n')

        desc = np.array(desc)
        print(desc.shape)

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
