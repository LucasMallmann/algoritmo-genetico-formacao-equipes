from app_api.genetic_algorithm.dna import Dna


class Population(object):
    def __init__(self, total_population: int):
        self.total_population = total_population
        self.population = []

    def generate_initial_population(self, total_of_groups: int, persons_by_group: int):
        for i in range(self.total_population):
            dna = Dna(total_of_groups, persons_by_group)
            self.population.append(dna)
