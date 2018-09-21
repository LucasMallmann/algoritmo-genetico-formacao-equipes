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
        genes = np.empty(self.total_of_persons)  # criando um espaço vazio na memória
        groups = np.arange(1, self.quantity_of_groups + 1)
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
        print('\n')
        print('*' * 100)
        # Matriz para armazenar a soma de cada Param para cada grupo
        sum_of_params_by_group = np.zeros(
            (len(parameters), self.quantity_of_groups))

        # Calcular a soma de cada param para cada grupo
        for param_idx, param_line in enumerate(parameters):

            for person_idx, group_number in enumerate(self.genes):
                sum_of_params_by_group[param_idx][group_number -
                                                  1] += param_line[person_idx]
            
        # print(sum_of_params_by_group)

        result = 0

        for line in sum_of_params_by_group:
            # result += abs(line[0] - line[1])
            for k in range(self.quantity_of_groups):
                for j in range(k, self.quantity_of_groups):
                    result += abs(line[k] - line[j])

        print('RESULT -> {}'.format(result))
        self.fitness = 1 / result
        print('FITNESS -> {}'.format(1 / result))
        print('*' * 100)
        print('\n')

    def crossover(self, partner):
        child = Dna(self.quantity_of_groups, self.persons_by_group)
        # Posição randomica para fazer o corte do array
        random_position = np.random.randint(self.total_of_persons)
        first = self.genes[:random_position]
        second = partner.genes[random_position:]
        print('POSICAO_DE_CORTE -> %s' %random_position)
        print(first)
        print(second)
        child.genes = first + second
        return child

    # def find_persons_by_group_id(self, group_id: int):
    #     persons_founded = []
    #     for person in self.persons:
    #         if person.group_id == group_id:
    #             persons_founded.append(person)
    #     return persons_founded

    # def fill_persons(self):
    #     """
    #     Preencher a lista com pessoas. As pessoas estão vindo de um arquivo json
    #     """
    #     person_names = PersonNames()
    #     persons = []
    #     for idx, group_id in enumerate(self.genes, start=1):
    #         name = person_names.search_name_by_id(idx)
    #         person = Person(name=name, person_id=idx, group_id=group_id)
    #         persons.append(person)
    #     return persons

    # def form_groups(self):
    #     """
    #     Busca as pessoas que tem certo group_id para formar os grupos
    #     """
    #     # Para contar de 1 até self.quantity_of_groups + 1
    #     # O range vai de x até y-1...
    #     for i in range(1, self.quantity_of_groups + 1):
    #         self.groups.append(self.find_persons_by_group_id(i))

    def __repr__(self):
        return 'numero dos grupos: %s' % self.genes + '\n'
