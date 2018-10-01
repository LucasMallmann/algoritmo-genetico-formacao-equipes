from random import randint
import random
import numpy as np
import statistics

from app_api.exceptions.invalid_groups import InvalidGroup
from app_api.genetic_algorithm.person import Person
from app_api.helpers.person_names_json import PersonNames


def generate_parameters(total_of_persons):
    return np.random.random_integers(
        1, 5, (3, total_of_persons))


class Dna(object):

    def __init__(self,
                 quantity_of_groups: int,
                 persons_by_group: int):

        self.quantity_of_groups = quantity_of_groups
        self.persons_by_group = persons_by_group
        self.total_of_persons = self.quantity_of_groups * self.persons_by_group
        # self.groups = []

        self.fitness = 0
        self.genes = self.fill_genes()
        # self.persons = self.fill_persons()
        # self.form_groups()

    def fill_genes(self) -> list:
        """
        Preencher a lista com números inteiros, representado
        os indexs dos grupos.
        :return: list
        """
        genes = np.empty(
            self.total_of_persons)  # criando um espaço vazio na memória
        groups = np.arange(self.quantity_of_groups)
        indexes = np.arange(len(genes))

        np.put(genes, indexes, groups)

        # converter os elementos dos genes para inteiro
        genes = [int(group_idx) for group_idx in genes]
        # random.shuffle(genes)  # desordenar o array
        np.random.shuffle(genes)

        return genes

    def calc_fitness(self, parameters: np.ndarray):
        """
        Função para calcular o fitness de cada indivíduo da população
        """
        # print('\n')
        # Matriz para armazenar a soma de cada Param para cada grupo
        sum_of_params_by_group = np.zeros(
            (len(parameters), self.quantity_of_groups))

        # Calcular a soma de cada param para cada grupo
        for param_idx, param_line in enumerate(parameters):

            for person_idx, group_number in enumerate(self.genes):
                sum_of_params_by_group[param_idx][group_number] += param_line[person_idx]

        result = 0

        for line in sum_of_params_by_group:
            # result += abs(line[0] - line[1])
            for k in range(self.quantity_of_groups):
                for j in range(k, self.quantity_of_groups):
                    result += abs(line[k] - line[j])

        self.fitness = 1 / result

    def crossover(self, partner, random_position: int):
        child1 = Dna(self.quantity_of_groups, self.persons_by_group)
        child2 = Dna(self.quantity_of_groups, self.persons_by_group)

        first_child1 = self.genes[:random_position]
        second_child1 = partner.genes[random_position:]

        first_child2 = self.genes[random_position:]
        second_child2 = partner.genes[:random_position]

        child1.genes = first_child1 + second_child1
        child2.genes = first_child2 + second_child2

        return (child1, child2)

    def mutate(self, mutation_rate):
        for i, gene in enumerate(self.genes):
            if random.random() < mutation_rate:
                pos = np.random.randint(self.total_of_persons)
                aux = self.genes[pos]
                self.genes[pos] = gene
                self.genes[i] = aux
                # print('mutated')

    def __repr__(self):
        return f'{self.genes}, fitness: {round(self.fitness, 2)}'
