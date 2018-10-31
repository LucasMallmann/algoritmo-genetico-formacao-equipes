from random import random, sample, choice, uniform
from math import floor
import numpy as np
from numpy import array, dot, mean
from numpy.linalg import pinv
from tqdm import tqdm
from pprint import PrettyPrinter
from sheets.spreadsheet import get_client

pp = PrettyPrinter()


def create_individual(individual_size: int):
    genes = np.empty(individual_size)
    groups = np.arange(total_groups)
    indexes = np.arange(len(genes))
    np.put(genes, indexes, groups)
    genes = [int(group_idx) for group_idx in genes]
    np.random.shuffle(genes)
    return genes


def create_population(individual_size: int, population_size: int):
    return [create_individual(individual_size) for i in range(population_size)]


def crossover(parent_1, parent_2):
    """
    Retorna os filhos dado dois pais.
    Os cromossomos não são necessariamente linkados
    """
    child = {}
    loci = [i for i in range(0, individual_size)]
    # 50% do tamanho do individuo
    loci_1 = sample(loci, floor(0.5 * (individual_size)))
    # Escolher todos que ainda não foram escolhidos no loci_1
    loci_2 = [i for i in loci if i not in loci_1]
    chromosome_1 = [[i, parent_1['individual'][i]] for i in loci_1]
    chromosome_2 = [[i, parent_2['individual'][i]] for i in loci_2]
    child.update({key: value for (key, value) in chromosome_1})
    child.update({key: value for (key, value) in chromosome_2})
    return [child[i] for i in loci]


def my_crossover(parent_1, parent_2, random_pos):
    child_1 = parent_1['individual'][:random_pos] + \
        parent_2['individual'][random_pos:]
    child_2 = parent_2['individual'][:random_pos] + \
        parent_1['individual'][random_pos:]
    return child_1, child_2


def mutate(individual):
    """
    Realizar a mutação de um indivíduo.

    """
    loci = [i for i in range(0, individual_size)]
    position_1 = sample(loci, 1)[0]
    position_2 = sample(loci, 1)[0]
    if position_2 != position_1:
        aux = individual[position_1]
        individual[position_1] = individual[position_2]
        individual[position_2] = aux
    return individual


def correct_individual(individual):
    '''
    Irá corrigir os indivíduos de uma população
    Ex: ALUNOS_POR_GRUPO = 3
        grupos = [0 ,0 ,0 ,0, 1, 1, 2, 2, 2]
        Irá arrumar para:
        [0, 0, 0, 1, 1, 1, 2, 2, 2]
    '''
    for group_number in range(total_groups):
        group_count = list(individual).count(group_number)
        if group_count > persons_by_group:
            while group_count != persons_by_group:
                rand_idx, rand_number = choice(
                    list(enumerate(individual)))
                if rand_number == group_number:
                    bigger = [x for x in individual if x > group_number]
                    if bigger:
                        individual[rand_idx] = choice(bigger)
                    else:
                        individual[rand_idx] = group_number + 1
                group_count = list(individual).count(group_number)

        if group_count < persons_by_group:
            while group_count != persons_by_group:
                rand_idx, rand_number = choice(
                    list(enumerate(individual)))
                if rand_number > group_number:
                    individual[rand_idx] = group_number
                group_count = list(individual).count(group_number)

    return individual


def check_termination_condition(best_individual):
    """
    Checar se o melhor indivíduo atual é melhor ou igual ao esperado
    """
    if ((best_individual.get('sum_result') <= 6)
            or (generation_count == max_generations)):
        return True
    else:
        return False


def get_offspring_new_population(current_population):
    """
    Irá obter uma parcela da nova população que será gerada
    """
    split_random_position = np.random.randint(1, individual_size)
    descendants_crossover = []

    amount_to_crossover = int(np.floor(crossover_rate * population_size))
    amount_to_mutate = int(np.floor(mutation_rate * population_size))

    for _ in range(amount_to_crossover):
        parent_1 = select_parent_roulette(current_population)
        parent_2 = select_parent_roulette(current_population)
        child_1, child_2 = my_crossover(parent_1,
                                        parent_2,
                                        split_random_position)
        child_1 = correct_individual(child_1)
        child_2 = correct_individual(child_2)
        descendants_crossover.append(child_1)
        descendants_crossover.append(child_2)

    individuals_to_mutate = sample(descendants_crossover,
                                   amount_to_mutate)
    descendants_mutated = [mutate(ind) for ind in individuals_to_mutate]

    descendants = descendants_crossover + descendants_mutated
    # Calcular o fitness dos novos descendentes
    descendants = calc_population_fitness(descendants, parameters)
    descendants = sorted(descendants, key=lambda i: i['sum_result'])

    total_to_select = population_size - amount_survived
    return descendants[:total_to_select]


def get_fitness(individual, parameters: np.ndarray) -> dict:
    '''
    Irá obter a fitness de cada indivíduo
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

    fitness = 1 / (result ** 2)
    return {'individual': individual, 'sum_result': result, 'fitness': fitness}


def calc_population_fitness(
        population: np.ndarray,
        parameters: np.ndarray):
    calculated_fit = [get_fitness(ind, parameters)
                      for ind in population]
    total_fit = sum([ind.get('fitness')
                     for ind in calculated_fit])
    for individual in calculated_fit:
        individual['fitness'] = individual['fitness'] / total_fit

    return calculated_fit


def get_new_generation(current_population, descendants):
    sorted_pop = sorted(current_population, key=lambda i: i['sum_result'])
    survived = sorted_pop[:amount_survived]
    # print('\n')
    # print(f'Survived = {survived}')
    return survived + descendants


def select_parent_roulette(population):
    """
    Irá selecionar um indivíduo para realizar o cruzamento
    através do método de roleta
    """
    pick = uniform(0, 1)
    current = 0
    for individual in population:
        current += individual.get('fitness')
        if current > pick:
            return individual


TP = [20, 50, 100, 150]
NG = [50, 100, 150, 200, 250, 300]
TC = [0.6, 0.7, 0.8, 0.9]
TM = [0.05, 0.1, 0.15, 0.20]
IG = [0, 0.1, 0.2, 0.3]

total_groups = 4
individual_size = 20
probability_of_individual_mutating = 0.1

import gspread
client = get_client(
    ['https://spreadsheets.google.com/feeds',
     'https://www.googleapis.com/auth/drive']
)

worksheet = client.open('Results - TG').sheet1

# Parâmetros genéticos
# population_size = 100
# max_generations = 100
# mutation_rate = 0.5
# crossover_rate = 0.7
# ig = 0.1

# persons_by_group = int(individual_size / total_groups)
# parameters = np.random.random_integers(
#     1, 5, (3, total_groups * persons_by_group))

# best_individuals_stash = [create_individual(individual_size)]
# initial_population = create_population(individual_size, population_size)
# termination = False
# generation_count = 0

# print(f'Parameters (Skills) = \n{parameters}')
# print('-' * 80)
# initial_population = calc_population_fitness(initial_population, parameters)
# current_population = initial_population
# [print(ind) for ind in initial_population]
# initial_best_ind = sorted(current_population, key=lambda i: i['sum_result'])[0]
# print(f'Initial best individual - {initial_best_ind}')
# print('-' * 50)

ag = 1

for population_size in TP:
    for max_generations in NG:
        for crossover_rate in TC:
            for mutation_rate in TM:
                for ig in IG:

                    print('Genetic Parameters')
                    print(f'AG number = {ag}')
                    print(f'Population Size - {population_size}')
                    print(f'Max Generations - {max_generations}')
                    print(f'Crossover Rate - {crossover_rate}')
                    print(f'Mutation Rate - {mutation_rate}')
                    print(f'Generation Increment (survival) - {ig}')

                    print('\n')

                    persons_by_group = int(individual_size / total_groups)
                    parameters = np.random.random_integers(
                        1, 5, (3, total_groups * persons_by_group))

                    best_individuals_stash = [create_individual(individual_size)]
                    initial_population = create_population(individual_size, population_size)
                    termination = False
                    generation_count = 0

                    # print(f'Parameters (Skills) = \n{parameters}')
                    pp.pprint(f'Parameters - {parameters}')
                    print('-' * 80)
                    initial_population = calc_population_fitness(initial_population, parameters)
                    current_population = initial_population
                    [print(ind) for ind in initial_population]
                    initial_best_ind = sorted(current_population, key=lambda i: i['sum_result'])[0]
                    print('\n')
                    print(f'Initial best individual - {initial_best_ind}')
                    print('-' * 50)
                    amount_survived = int(np.floor(ig * population_size))

                    while termination is False:
                        descendants = get_offspring_new_population(current_population)
                        new_generation = get_new_generation(current_population, descendants)

                        gen_fit = sum([n['fitness'] for n in new_generation])
                        new_individuals = [ind['individual'] for ind in new_generation]
                        current_population = calc_population_fitness(new_individuals, parameters)

                        # [pp.pprint(ind) for ind in current_population]

                        best_individual = sorted(
                            current_population, key=lambda i: i['sum_result'])[0]
                        termination = check_termination_condition(best_individual)
                        generation_count += 1
                        print(f'Best Individual = {best_individual}')
                        print('\n')

                    # line = [
                    #     ag, population_size, max_generations, crossover_rate, mutation_rate, ig,
                    #     initial_best_ind['individual'], initial_best_ind['sum_result'],
                    #     best_individual['individual'], best_individual['sum_result'],
                    # ]

                    line = [
                        ag, population_size, max_generations, crossover_rate, mutation_rate, ig,
                        str(initial_best_ind['individual']), str(initial_best_ind['sum_result']),
                        str(best_individual['individual']), str(best_individual['sum_result']),
                    ]
                    
                    worksheet.append_row(line)

                    ag += 1

                    print('\n')
                    print('\n')



# for i in range(max_generations):
#     descendants = get_offspring_new_population(current_population)
#     new_generation = get_new_generation(current_population, descendants)

#     gen_fit = sum([n['fitness'] for n in new_generation])
#     new_individuals = [ind['individual'] for ind in new_generation]
#     current_population = calc_population_fitness(new_individuals, parameters)

#     [pp.pprint(ind) for ind in current_population]

#     best_individual = sorted(
#         current_population, key=lambda i: i['sum_result'])[0]

#     print(f'Best Individual = {best_individual}')
#     print('\n')
