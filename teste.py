import numpy as np
from pprint import PrettyPrinter

pp = PrettyPrinter()

def get_fitness(individual, parameters: np.ndarray) -> dict:
    '''
    Irá obter a fitness de cada indivíduo
    '''
    sum_of_params_by_group = np.zeros(
        (len(parameters), total_groups))
    for param_idx, param_line in enumerate(parameters):
        for person_idx, group_number in enumerate(individual):
            sum_of_params_by_group[param_idx][group_number] += param_line[person_idx]

    pp.pprint(sum_of_params_by_group)


    result = 0
    for line in sum_of_params_by_group:
        for k in range(total_groups):
            for j in range(k, total_groups):
                result += abs(line[k] - line[j])

    fitness = 1 / (result ** 2)
    return {'individual': individual, 'fitness': result, 'probability': fitness}


total_groups = 3

parameters = [
	[5, 4, 3, 4, 2, 3, 7, 4, 5],
	[2, 5, 4, 1, 1, 4, 3, 2, 1],
	[3, 4, 3, 2, 2, 5, 5, 4, 1]
]


individual = [0, 2, 1, 2, 1, 0 ,0 ,2, 1]
fit = get_fitness(individual, parameters)
print(fit)