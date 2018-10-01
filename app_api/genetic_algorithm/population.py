from app_api.genetic_algorithm.dna import Dna
import numpy as np
import random


def generate_parameters(total_of_persons):
    return np.random.random_integers(
        1, 5, (3, total_of_persons))


class Population(object):
    def __init__(self, total_population: int,
                 mutation_rate: float,
                 crossover_rate: float,
                 survival_rate: float):
        self.total_population = total_population
        self.population = []
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.survival_rate = survival_rate
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

    def average_fitness(self):
        total = 0
        for individual in self.population:
            total += individual.fitness
        return total / self.total_population

    def crossover(self, dna1: Dna, dna2: Dna, split_position: int):
        child1 = Dna(self.total_of_groups, self.persons_by_group)
        child2 = Dna(self.total_of_groups, self.persons_by_group)
        child1.genes = dna1.genes[:split_position] + \
            dna2.genes[split_position:]
        child2.genes = dna2.genes[:split_position] + \
            dna1.genes[split_position:]

        return child1, child2

    def get_mutated_individuals(self, container: list):
        '''
        Irá obter os indivíduos para realizar a mutação
        @param container - Irá obter os indivíduos mutados desse container
        '''
        amount_to_mutate = round(self.total_population * self.mutation_rate)
        mutateds = []
        for m in range(amount_to_mutate):
            mutated_individual = self.select_best_dna(container)
            mutated_individual.mutate(self.mutation_rate)
            mutated_individual.calc_fitness(self.PARAMETERS)
            mutateds.append(mutated_individual)
        return mutateds

    def generate_descendants(self):
        '''
        Irá gerar os descendetes para gerar uma nova população
        '''
        descendants = []
        total_persons = self.persons_by_group * self.total_of_groups
        split_random_position = np.random.randint(1, total_persons)
        amount_of_crossing = round(self.total_population * self.crossover_rate)

        for i in range(amount_of_crossing):
            parent1 = self.select_best_dna(self.population)
            parent2 = self.select_best_dna(self.population)
            childs = self.crossover(parent1, parent2, split_random_position)
            child1 = childs[0]
            child2 = childs[1]
            # Calcular o fitness
            child1.calc_fitness(self.PARAMETERS)
            child2.calc_fitness(self.PARAMETERS)
            descendants.append(child1)
            descendants.append(child2)
        return descendants

    def correct_individuals(self, descendants: list):
        '''
        Irá corrigir os indivíduos de uma população
        Ex: ALUNOS_POR_GRUPO = 3
            grupos = [0 ,0 ,0 ,0, 1, 1, 2, 2, 2]
            Irá arrumar para:
            [0, 0, 0, 1, 1, 1, 2, 2, 2]
        '''
        for line_idx, individual in enumerate(descendants):
            for group_number in range(self.total_of_groups - 1):
                group_count = list(individual.genes).count(group_number)

                if group_count > self.persons_by_group:
                    while group_count != self.persons_by_group:
                        rand_idx, rand_number = random.choice(
                            list(enumerate(individual.genes)))
                        if rand_number == group_number:
                            individual.genes[rand_idx] = random.choice(
                                [x for x in individual.genes if x > group_number])
                        group_count = list(
                            individual.genes).count(group_number)

                if group_count < self.persons_by_group:
                    while group_count != self.persons_by_group:
                        rand_idx, rand_number = random.choice(
                            list(enumerate(individual.genes)))
                        if rand_number > group_number:
                            individual.genes[rand_idx] = group_number
                        group_count = list(
                            individual.genes).count(group_number)
        return descendants

    def generate(self) -> list:
        '''
        Irá gerar os descendentes da população.
        Esses descendentes serão escolhidos para formarem uma nova população
        '''
        amount_survived = round(self.total_population * self.survival_rate)

        descendants = self.generate_descendants()
        descendants = self.correct_individuals(descendants)

        mutated_individuals = self.get_mutated_individuals(descendants)
        for mutated in mutated_individuals:
            descendants.append(mutated)

        survived = []
        for k in range(amount_survived):
            survived_individual = self.select_best_dna(self.population)
            survived.append(survived_individual)

        # SELECIONAR DOS DESCENDENTES
        total_to_select_from_descendants = len(
            self.population) - amount_survived - len(mutated_individuals)

        selected_descendants = []
        for j in range(total_to_select_from_descendants):
            selected_descendant = self.select_best_dna(descendants)
            selected_descendants.append(selected_descendant)

        self.generations += 1
        self.population = survived + selected_descendants + mutated_individuals

        # Calcular a Fitness da nova população
        self.calc_fitness()
        return self.population

    def select_best_dna(self, dna_container) -> Dna:
        """
        Irá selecionar o melhor individuo dentro de um conjunto de individuos
        """
        total = sum([individual.fitness for individual in dna_container])
        pick = random.uniform(0, total)
        current = 0
        for i, individual in enumerate(dna_container):
            current += individual.fitness
            if current > pick:
                return individual
