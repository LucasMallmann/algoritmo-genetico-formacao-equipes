from app_api.genetic_algorithm.population import Population
from app_api.genetic_algorithm.dna import Dna
import json

TOTAL_GROUPS = 2
PERSONS_BY_GROUP = 3
TP = 50
CROSSOVER_RATE = 0.9
MUTATION_RATE = 0.2
SURVIVAL_POPULATION_RATE = 0.2
TOTAL_GENERATIONS = 500


def save_to_json(population: Population):
    dict_data = {
        'Generation': population.generations,
        'Population': []
    }
    for individual in population.population:
        dict_data['Population'].append({
            'genes': individual.genes,
            'fitness': round(individual.fitness, 2)
        })

    with open('results.json', 'a', encoding='utf-8') as j:
        json.dump(dict_data, j)


def main():
    population = Population(
        total_population=TP,
        mutation_rate=MUTATION_RATE,
        crossover_rate=CROSSOVER_RATE,
        survival_rate=SURVIVAL_POPULATION_RATE
    )
    population.generate_initial_population(TOTAL_GROUPS, PERSONS_BY_GROUP)
    population.calc_fitness()

    for ind in population.population:
        print(ind)
    print(f'Average Fitness - {round(population.average_fitness(), 2)}')

    # save_to_json(population)

    print('\n')

    for tg in range(TOTAL_GENERATIONS):
        population.generate()
        population.calc_fitness()
        for new in population.population:
            print(new)
        print(f'Average Fitness - {round(population.average_fitness(), 2)}')
        print(f'Generation: {population.generations}')
        print('\n')
        # save_to_json(population)


if __name__ == '__main__':
    main()
