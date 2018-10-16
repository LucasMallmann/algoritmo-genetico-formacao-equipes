from random import random, sample, choice, uniform
from math import floor
import numpy as np
from numpy import array, dot, mean
from numpy.linalg import pinv
from tqdm import tqdm


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


def evaluate_population(population):
    '''
    Avalia uma populaçõa de indivíduos e retorna os melhores entre eles.
    '''
    fitness_list = [get_fitness(individual, parameters)
                    for individual in tqdm(population)]
    sum_list = sorted(fitness_list, key=lambda i: i.get('sum_result'))
    # [print(fit) for fit in fitness_list]
    # print('\n')
    # [print(best) for best in sum_list]
    best_individuals = sum_list[:selection_size]
    best_individuals_stash.append(best_individuals[0]['individual'])
    print(f"Sum [Error] {best_individuals[0]['sum_result']} \
            Fitness {best_individuals[0]['fitness']}")
    return best_individuals


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


def mutate(individual):
    """
    Realizar a mutação de um indivíduo.

    """
    loci = [i for i in range(0, individual_size)]
    no_of_genes_mutated = floor(probability_of_gene_mutating * individual_size)
    # loci_to_mutate = sample(loci, no_of_genes_mutated)
    for _ in range(no_of_genes_mutated):
        position_1 = sample(loci, 1)[0]
        position_2 = sample(loci, 1)[0]
        if position_2 != position_1:
            aux = individual[position_1]
            individual[position_1] = individual[position_2]
            individual[position_2] = aux
    return individual


def check_termination_condition(best_individual):
    """
    Checar se o melhor indivíduo atual é melhor ou igual ao esperado
    """
    if ((best_individual.get('fitness') >= 0.6)
            or (generation_count == max_generations)):
        return True
    else:
        return False


def get_new_generation(selected_individuals):
    """
    Dado os indivíduos selecionados, crie uma nova população realizando os cruzamentos
    Aqui nós colocaremos variações como cruzamento e mutação
    """
    parent_pairs = [sample(selected_individuals, 2)
                    for i in range(population_size)]
    offspring = [crossover(pair[0], pair[1]) for pair in parent_pairs]
    offspring_indices = [i for i in range(population_size)]
    offspring_to_mutate = sample(
        offspring_indices,
        floor(probability_of_individual_mutating*population_size)
    )
    mutated_offspring = [[i, mutate(offspring[i])]
                         for i in offspring_to_mutate]
    for child in mutated_offspring:
        offspring[child[0]] = child[1]
    return offspring


def get_fitness(individual, parameters: np.ndarray) -> dict:
    '''
    Irá obter a fitness de cada indivíduo
    '''
    sum_of_params_by_group = np.zeros(
            (len(parameters), total_groups))
    for param_idx, param_line in enumerate(parameters):
        for person_idx, group_number in enumerate(individual):
            sum_of_params_by_group[param_idx] \
                                        [group_number] += param_line[person_idx]
    
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
    sum_fitness = 0
    calculated_fit = [get_fitness(ind, parameters)
                        for ind in population]
    total_fit = sum([ind.get('fitness') 
                for ind in calculated_fit])
    for individual in calculated_fit:
        individual['fitness'] = individual['fitness'] / total_fit

    return calculated_fit


def select_parent_roulette(population):
    """
    Irá selecionar indivíduos para fazer o cruzamento
    """
    pick = uniform(0, 1)
    current = 0
    for individual in population:
        current += individual.get('fitness')
        if current > pick:
            return individual


total_groups = 3
population_size = 10
individual_size = 9
probability_of_individual_mutating = 0.1
max_generations = 50
probability_of_gene_mutating = 0.25
persons_by_group = int(individual_size / total_groups)
parameters = np.random.random_integers(1, 10, (3, total_groups * persons_by_group))
selection_size = int(np.floor(0.1 * population_size))
best_individuals_stash = [create_individual(individual_size)]
initial_population = create_population(individual_size, population_size)
current_population = initial_population
termination = False
generation_count = 0

print(f'Parameters = \n{parameters}')
print('-' * 80)
# individual = create_individual(individual_size)
# print(f'{individual} - individual')
# fitness = get_fitness(individual, parameters)
# print(f"fitness - {fitness.get('fitness')}")

print(initial_population)
calculated_population = calc_population_fitness(initial_population, parameters)
[print(ind) for ind in calculated_population]
to_mutate = select_parent_roulette(calculated_population)
print('-' * 30 + 'To Mutate' + '-' * 30)
print(to_mutate)
# while termination is False:
#     current_best_individual = get_fitness(best_individuals_stash[-1], parameters)
#     print(f'Generation : {generation_count}')
#     best_individuals = evaluate_population(current_population)
#     current_population = get_new_generation(best_individuals)
#     termination = check_termination_condition(current_best_individual)
#     generation_count += 1
# else:
#     print(get_fitness(best_individuals_stash[-1], parameters))
