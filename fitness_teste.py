import random
import numpy as np


def create_individual(individual_size: int):
    genes = np.empty(individual_size)
    groups = np.arange(total_groups)
    indexes = np.arange(len(genes))
    np.put(genes, indexes, groups)
    genes = [int(group_idx) for group_idx in genes]
    np.random.shuffle(genes)
    return genes


def create_skills(individual) -> list:
    indexes = [i for i, _ in enumerate(individual)]
    # skills = []
    # skills[:] = [{
    #     i: random.sample(range(1, 6), 3)
    # } for i in indexes]
    skills = {i: random.sample(range(1, 6), 3) for i in indexes}
    return skills


def calc_fitness(individual: np.array, parameters):
    '''
    Calcular a fitness do indivíduo para cada grupo
    '''
    sum_of_params_by_group = np.zeros(
            (len(parameters), total_groups))

    for param_idx, param_line in enumerate(parameters):
        for person_idx, group_number in enumerate(individual):
            sum_of_params_by_group[param_idx][group_number] += param_line[person_idx]

    result = 0

    for line in sum_of_params_by_group:
        for k in range(total_groups):
            for j in range(k, total_groups):
                result += abs(line[k] - line[j])

    print(f'fit without square = {1 / result}')
    fitness = 1 / (result ** 2)

    print(f'Result - {result}')
    print(f'fitness - {fitness}')
    print('\n')

    return fitness



PARAMETERS = [[3, 1, 4, 1, 4, 1, 5, 3, 4],
              [5, 3, 4, 5, 5, 1, 2, 4, 4],
              [5, 5, 3, 1, 5, 5, 3, 1, 2]]


individual_size = 9
total_groups = 3

# individual = create_individual(individual_size)
# print(individual)
# skills = create_skills(individual)
# print(skills)
# print('-'*50)
# calc_fitness(individual, skills)
ind_1 = [2, 2, 0, 0, 1, 1, 2, 0, 1]
ind_2 = [1, 2, 1, 1, 0, 2, 0, 2, 0]

s = []
s.append(calc_fitness(ind_1, PARAMETERS))
s.append(calc_fitness(ind_2, PARAMETERS))

sm = sum(s)
print(s)
sm_div = np.array(s/sm)

print(sm_div)
