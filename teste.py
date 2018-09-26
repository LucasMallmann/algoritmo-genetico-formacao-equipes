from app_api.genetic_algorithm.population import Population
from app_api.genetic_algorithm.dna import Dna
import numpy as np

total_groups = 2
persons_by_group = 3
TP = 20
CROSSOVER_RATE = 0.7
MUTATION_RATE = 0.1

population = Population(
    total_population=TP,
    mutation_rate=MUTATION_RATE,
    crossover_rate=CROSSOVER_RATE
)

population.generate_initial_population(total_groups, persons_by_group)

pop = population.population

print('-' * 40)
print('\t' + 'População Inicial')
for p in pop:
    print(p)
print('-' * 40)

population.calc_fitness()

print('-' * 40 + 'FIM DO FITNESS' + '-' * 40)

population.generate()
