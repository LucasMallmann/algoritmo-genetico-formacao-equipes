from random import randint
import numpy as np

from app_api.exceptions.invalid_groups import InvalidGroup
from app_api.genetic_algorithm.person import Person
from app_api.helpers.person_names_json import PersonNames


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
        groups = np.arange(1, self.quantity_of_groups + 1)
        indexes = np.arange(len(genes))

        np.put(genes, indexes, groups)

        # converter os elementos dos genes para inteiro
        genes = [int(group_idx) for group_idx in genes]

        return genes

    def calc_fitness(self):
        pass

    def find_persons_by_group_id(self, group_id: int):
        persons_founded = []
        for person in self.persons:
            if person.group_id == group_id:
                persons_founded.append(person)
        return persons_founded

    def fill_persons(self):
        """
        Preencher a lista com pessoas. As pessoas estão vindo de um arquivo json
        """
        person_names = PersonNames()
        persons = []
        for idx, group_id in enumerate(self.genes, start=1):
            name = person_names.search_name_by_id(idx)
            person = Person(name=name, person_id=idx, group_id=group_id)
            persons.append(person)
        return persons

    def form_groups(self):
        """
        Busca as pessoas que tem certo group_id para formar os grupos
        """
        # Para contar de 1 até self.quantity_of_groups + 1
        # O range vai de x até y-1...
        for i in range(1, self.quantity_of_groups + 1):
            self.groups.append(self.find_persons_by_group_id(i))
