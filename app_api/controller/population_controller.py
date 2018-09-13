from app_api.genetic_algorithm.population import Population
from app_api.genetic_algorithm.dna import Dna

# Está 'hardcoded'. Modificar para passar dinamicamente
total_groups = 6
persons_by_group = 5
# total_persons = 28
# minimum_of_persons = 6
TP = 50


class PopulationController(object):
    def build_population(self) -> Population:
        """

        :rtype: Population
        """
        population = Population(total_population=TP)
        population.generate_initial_population(total_groups, persons_by_group)

        return population
