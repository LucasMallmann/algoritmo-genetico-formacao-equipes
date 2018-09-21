from app_api.genetic_algorithm.population import Population
from app_api.genetic_algorithm.dna import Dna
import numpy as np

total_groups = 4
persons_by_group = 5
TP = 10
MUTATION_RATE = 0.7

population = Population(total_population=TP, mutation_rate=MUTATION_RATE)
population.generate_initial_population(total_groups, persons_by_group)

pop = population.population

print('-' * 100)
print(pop)
print('-' * 100)

population.calc_fitness()

print('-' * 40 + 'FIM DO FITNESS' + '-' * 40)
generated = population.generate()

print('\n')

print('NOVA POPULAÇÃO')

for ind in generated:
    print(ind)
