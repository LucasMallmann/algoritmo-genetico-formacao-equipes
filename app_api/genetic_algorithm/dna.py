from random import randint
from app_api.exceptions.invalid_groups import InvalidGroup
from app_api.genetic_algorithm.person import Person
from app_api.helpers.person_names_json import PersonNames


class Dna(object):
    def __init__(self,
                 quantity_of_persons: int,
                 quantity_of_groups: int,
                 minimum_of_persons: int):

        self.quantity_of_persons = quantity_of_persons
        self.quantity_of_groups = quantity_of_groups
        self.minimum_of_persons = minimum_of_persons
        self.groups = []

        self.genes = self.fill_genes()
        self.persons = self.fill_persons()
        self.form_groups()

    def fill_genes(self) -> list:
        """
        Preencher a lista com números inteiros, representado
        os indexs dos grupos.
        :return: list
        """
        genes = []

        if self.quantity_of_groups * self.minimum_of_persons > self.quantity_of_persons:
            raise InvalidGroup('Não há pessoas suficientes para formar os grupos')

        for i in range(self.quantity_of_persons):
            random_number = randint(1, self.quantity_of_groups)
            genes.append(random_number)

        return genes

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
            
