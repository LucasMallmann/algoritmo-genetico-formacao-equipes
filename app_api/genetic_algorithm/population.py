from app_api.genetic_algorithm.dna import Dna


class Population(object):

    def __init__(self, quantity_of_groups: int):
        self.quantity_of_groups = quantity_of_groups
        self.population = []
        self.generate_initial_populate()

    def generate_initial_populate(self):
        """
        Gerar a população inicial com vários Dnas
        :return:
        """
        for i in range(self.quantity_of_groups):
            persons = 5
            persons_dna = Dna(quantity_of_persons=persons)
            self.population.append(persons_dna)
