from app_api.genetic_algorithm.population import Population
from app_api.genetic_algorithm.dna import Dna

# Não está utilizando essas listas ainda
TP_LIST = [20, 50, 100, 200, 500]
TC_LIST = [0.6, 0.7, 0.8, 0.9]
MUTATION_RATE_LIST = [0.01, 0.05, 0.1, 0.2]
TOTAL_GENERATIONS_LIST = [20, 50, 100, 200, 500, 1000]

TOTAL_GROUPS = 3
PERSONS_BY_GROUP = 3
TP = 10
CROSSOVER_RATE = 0.6
MUTATION_RATE = 0.1
SURVIVAL_POPULATION_RATE = 0.2
TOTAL_GENERATIONS = 200


def main():
    # Geração da População inicial
    population = Population(total_population=TP,
                            mutation_rate=MUTATION_RATE,
                            crossover_rate=CROSSOVER_RATE,
                            survival_rate=SURVIVAL_POPULATION_RATE)

    population.generate_initial_population(TOTAL_GROUPS, PERSONS_BY_GROUP)
    population.calc_fitness()

    for ind in population.population:
        print(ind)

    print('-' * 100)
    selected_individual = population.roulette_selection(population.population)

    fit = [individual.fitness for individual in population.population]
    print(sum(fit))

    # print(f'Average Fitness - {round(population.average_fitness(), 2)}')
    # print('\n')
        
    # for tg in range(TOTAL_GENERATIONS):
    #     population.generate() # gerar uma nova população
    #     population.calc_fitness() # calcular o fitness de cada individuo
    #     for new in population.population:
    #         print(new)
    #     print(f'Average Fitness - {round(population.average_fitness(), 2)}')
    #     print(f'Generation: {population.generations}')
    #     print('\n')


if __name__ == '__main__':
    main()
