from app_api.genetic_algorithm.population import Population


class PopulationController(object):
    def build_population(self) -> Population:
        """

        :rtype: Population
        """
        # Está 'hardcoded'. Modificar para passar dinamicamente
        total_groups = 4
        total_persons = 28
        minimum_of_persons = 6
        TP = 50

        population = Population(total_population=TP)

        population.generate_initial_population(total_persons, total_groups, minimum_of_persons)

        print('-' * 100)
        for gene in population.population:
            print('\n')
            print('-' * 40 + 'BEGIN OF INDIVIDUAL' + '-' * 40)
            for person in gene.find_persons_by_group_id(3):
                print(person)
            print('-' * 40 + 'END OF INDIVIDUAL' + '-' * 40)
            print('\n')
        print('-' * 100)

        return population
