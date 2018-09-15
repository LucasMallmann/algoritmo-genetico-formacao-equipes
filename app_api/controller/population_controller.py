from app_api.genetic_algorithm.population import Population
from app_api.genetic_algorithm.dna import Dna
import numpy as np

# Está 'hardcoded'. Modificar para passar dinamicamente
total_groups = 2
persons_by_group = 3


TP = 25


class PopulationController(object):
    def build_population(self) -> Population:
        """

        :rtype: Population
        """
        population = Population(total_population=TP)
        population.generate_initial_population(total_groups, persons_by_group)
        population.calc_fitness()

        return population.population
