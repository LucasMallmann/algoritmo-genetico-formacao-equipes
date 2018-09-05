from app_api.genetic_algorithm.dna import Dna


class Population(object):
    def __init__(self, total_population: int):
        self.total_population = total_population
        self.population = []

    def generate_initial_population(self, quantity_of_persons: int,
                                    quantity_of_groups: int,
                                    minimum_of_persons: int
                                    ):
        for i in range(self.total_population):
            dna = Dna(quantity_of_persons, quantity_of_groups, minimum_of_persons)
            self.population.append(dna)

