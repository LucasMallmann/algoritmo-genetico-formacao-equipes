from app_api.genetic_algorithm.person import  Person


class Dna(object):
    def __init__(self, quantity_of_persons: int):
        self.quantity_of_persons = quantity_of_persons
        self.genes = []
        self.fitness = 0
        self.fill_genes()

    def fill_genes(self):
        """
        Preencher o Dna com várias pessoas
        :return:
        """
        for i in range(self.quantity_of_persons):
            person = Person('Some random name...')
            self.genes.append(person)
