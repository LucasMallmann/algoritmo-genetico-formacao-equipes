from app_api.genetic_algorithm.population import Population
from app_api.genetic_algorithm.dna import Dna
import json

TP_LIST = [20, 50, 100, 200, 500]
TC_LIST = [0.6, 0.7, 0.8, 0.9]
CROSSOVER_RATE_LIST = [0.01, 0.05, 0.1, 0.2]
TOTAL_GENERATIONS_LIST = [20, 50, 100, 200, 500, 1000]

TOTAL_GROUPS = 5
PERSONS_BY_GROUP = 4
TP = 50
CROSSOVER_RATE = 0.7
MUTATION_RATE = 0.1
SURVIVAL_POPULATION_RATE = 0.2
TOTAL_GENERATIONS = 500


def main():
    for TP in TP_LIST:
        for TC in TC_LIST:
            for CROSSOVER in CROSSOVER_RATE_LIST:
                for NG in TOTAL_GENERATIONS_LIST:
                    pass

    population = Population(total_population=TP,
                            mutation_rate=MUTATION_RATE,
                            crossover_rate=CROSSOVER_RATE,
                            survival_rate=SURVIVAL_POPULATION_RATE)

    population.generate_initial_population(TOTAL_GROUPS, PERSONS_BY_GROUP)
    population.calc_fitness()

    for ind in population.population:
        print(ind)
    print(f'Average Fitness - {round(population.average_fitness(), 2)}')
    print('\n')
    for tg in range(TOTAL_GENERATIONS):
        population.generate()
        population.calc_fitness()
        for new in population.population:
            print(new)
        print(f'Average Fitness - {round(population.average_fitness(), 2)}')
        print(f'Generation: {population.generations}')
        print('\n')


if __name__ == '__main__':
    main()
