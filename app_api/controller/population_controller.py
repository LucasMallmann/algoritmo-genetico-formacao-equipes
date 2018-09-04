from app_api.genetic_algorithm.population import Population


class PopulationController(object):
    def build_population(self) -> Population:
        """

        :rtype: Population
        """
        # Está 'hardcoded'. Modificar para passar dinamicamente
        total_groups = 10
        population = Population(quantity_of_groups=total_groups)
        return population

