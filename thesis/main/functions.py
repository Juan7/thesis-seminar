"""Contain the functions for main app."""

import json
import pprint
from statistics import mean

from random import random, uniform, randint

from django.conf import settings


def generate_init_data(elements_amount, elements_size):
    """Generate random data."""
    result = []
    for i in range(elements_amount):
        item = [uniform(0, 100) for j in range(elements_size)]
        result.append(item)
    return result


def load_init_data():
    """Loads or generate random data."""
    try:
        with open('../fixtures/init_data.txt', 'r') as json_data:
            data = json.loads(json_data.read()).get('init_data')
    except Exception as e:
        print(e)
        data = generate_init_data(20, 4)
        json_data = json.dumps({'init_data': data})
        init_data = open('../fixtures/init_data.txt','w')
        init_data.write(json_data)
        init_data.close()
    return data


def get_random_diff_than(taken_indexes, data):
    """Get a random index that is not taken."""
    rand_index = randint(0, len(data) - 1)
    while rand_index in taken_indexes:
        rand_index = randint(0, len(data) - 1)
    taken_indexes.append(rand_index)
    return rand_index


def substract_array(array_1, array_2):
    """Substract element to element on same size arrays."""
    return [array_1[index] - array_2[index] for index, value in enumerate(array_1)]


def sum_array(array_1, array_2):
    """Sum element to element on same size arrays."""
    return [array_1[index] + array_2[index] for index, value in enumerate(array_1)]


def scalar_multiply_array(scalar, array):
    """Multiply an scalar to an array."""
    return [scalar * array[index] for index, value in enumerate(array)]


def get_mutate_data(data):
    """Get mutate data according on differential evolution method."""
    mutate_data = []
    for index, item in enumerate(data):
        taken_indexes = [index]
        index_0 = get_random_diff_than(taken_indexes, data)
        index_1 = get_random_diff_than(taken_indexes, data)
        index_2 = get_random_diff_than(taken_indexes, data)

        mutate_vector = sum_array(
                            data[index_0],
                            scalar_multiply_array(settings.SCALE_FACTOR, substract_array(data[index_1],data[index_2])))
        mutate_data.append(mutate_vector)
    return mutate_data


def get_crossover_data(data, mutate_data):
    """Get crossover data."""
    crossover_data = []
    for index, item in enumerate(data):
        crossover_vector = mutate_data[index] if random() < settings.CROSSOVER_RATE else data[index]
        crossover_data.append(crossover_vector)
    return crossover_data


def evaluate_multi_fitness(data):
    """Apply all th fitness we need."""
    item_1 = data[0:2]
    item_2 = data[2:4]
    fitness_item_1 = sum_fitness(item_1)
    fitness_item_2 = minus_fitness(item_2)
    return fitness_item_1, fitness_item_2


def dominate(item_1_data, item_1_results, item_2_data, item_2_results):
    """Dominate on arrays."""
    if item_1_results[0] > item_2_results[0] and item_1_results[1] < item_2_results[1]:
        return item_1_data
    elif item_1_results[0] < item_2_results[0] and item_1_results[1] > item_2_results[1]:
        return item_2_data
    else:
        return item_1_data if random() < 0.5 else item_2_data


def pareto_optimal(item_1, item_2):
    """Check what element dominates."""
    item_1_results = evaluate_multi_fitness(item_1)
    item_2_results = evaluate_multi_fitness(item_2)

    item_1_data = {'item': item_1, 'fitness': item_1_results}
    item_2_data = {'item': item_2, 'fitness': item_2_results}

    return dominate(item_1_data, item_1_results, item_2_data, item_2_results)


def pareto_compares(item_1, item_2):
    """Return the compares between 2 arrays."""
    return item_1[0] > item_2[0] and item_1[1] < item_2[1]

def sum_fitness(data):
    """Fitness function."""
    return sum(item for item in data) / mean(data)
#    return sum(item for item in data)


def minus_fitness(data):
    """Fitness function."""
#    diff = 0
#    for item in data:
#        diff -= item
    return mean(data)


def evaluate_fitness(data, crossover_data):
    """Get the next generation children using fitness function."""
    next_generation_data = []
    next_generation_fitness = []
    best = None
    best_item = None
    for index, item in enumerate(data):
        current_generation_data = pareto_optimal(data[index], crossover_data[index])
        # data_fitness = fitness(data[index])
        # crossover_fitness = fitness(crossover_data[index])
        # if data_fitness > crossover_fitness:
        #     best_fitness = data_fitness
        #     next_genetation_item = data[index]
        # else:
        #     best_fitness = crossover_fitness
        #     next_genetation_item = crossover_data[index]

        if not best or pareto_compares(current_generation_data['fitness'], best):
            best = current_generation_data['fitness']
            best_item = current_generation_data['item']
        next_generation_data.append(current_generation_data['item'])
        next_generation_fitness.append(current_generation_data['fitness'])
    return next_generation_data, next_generation_fitness, best_item, best


def get_random_indexes(index, item):
    taken_indexes = [index]
    first_index = randint(0, len(item) - 1)
    while first_index in taken_indexes:
        first_index = randint(0, len(item) - 1)
    taken_indexes.append(first_index)
    second_index = randint(0, len(item) - 1)
    while second_index in taken_indexes:
        second_index = randint(0, len(item) - 1)
    taken_indexes.append(second_index)
    return first_index, second_index


def get_new_item(index, item, data):
    first_index, second_index = get_random_indexes(index, data)
    mutate_vector = sum_array(
        data[index],
        scalar_multiply_array(settings.SCALE_FACTOR, substract_array(data[first_index],data[second_index])))
    crossover_vector = get_crossover_data(item, mutate_vector)
    return crossover_vector

def dominance(item, crossover_vector):
    result = {
        'state': False,
        'vector': None,
        'position': 0
    }
    
    item_fitness_1 = sum_fitness(item)
    item_fitness_2 = minus_fitness(item)
    crossover_vector_fitness_1 = sum_fitness(crossover_vector)
    crossover_vector_fitness_2 = minus_fitness(crossover_vector)
    
    if item_fitness_1 < crossover_vector_fitness_1 and item_fitness_2 < crossover_vector_fitness_2:
        result['state'] = True
        result['vector'] = item
        result['position'] = 1
    if crossover_vector_fitness_1 < item_fitness_1 and crossover_vector_fitness_2 < item_fitness_2:
        result['state'] = True
        result['vector'] = crossover_vector
        result['position'] = 2
    return result

def update_pareto_frontier(current, pareto_frontier):
    win = True
    new_frontier = []
    for pareto in pareto_frontier:
        dominance_data = dominance(current, pareto)
        if not dominance_data['state']:
            continue
        if dominance_data['position'] == 2:
            win = False

    if win:
        for pareto in pareto_frontier:
            dominance_data = dominance(current, pareto)
            if dominance_data['position'] == 1:
                continue
            else:
                new_frontier.append(pareto)
        new_frontier.append(current)
    else:
        new_frontier = list(pareto_frontier)
        
    b_set = set(tuple(x) for x in new_frontier)
    b = [ list(x) for x in b_set ]
    return b


def fitness_vector(pareto_frontier):
    fitness_data = []
    for pareto in pareto_frontier:
        fitness_data.append((sum_fitness(pareto), minus_fitness(pareto)))
    return fitness_data


def differential_evolution(generations, data):
    """Apply differential evolution on a dataset."""
    result_data = {
        'generations': [],
        'pareto_frontier': [],
        'best': None,
    }
    current_data = data

    pareto_frontier = []
    result_data['generations'].append(fitness_vector(current_data))
    for generation in range(generations):
        print(generation)
        next_generation_data = []
        for index, item in enumerate(current_data):
            crossover_vector = get_new_item(index, item, current_data)
            dominance_data = dominance(item, crossover_vector)
            while not dominance_data['state']:
                crossover_vector = get_new_item(index, crossover_vector, current_data)
                dominance_data = dominance(item, crossover_vector)
            winner_vector = dominance_data['vector']
            next_generation_data.append(winner_vector)
            pareto_frontier = update_pareto_frontier(winner_vector, pareto_frontier)
        current_data = next_generation_data
#        dominating = dominate(current_data, crossover_data)
#        mutate_data = get_mutate_data(current_data)
#        crossover_data = get_crossover_data(current_data, mutate_data)
#        next_generation_data, next_generation_fitness, best_item, best = evaluate_fitness(current_data, crossover_data)
        
        
#        generation_data = []
#        for index, item in enumerate(next_generation_data):
#            generation_data.append({
#                'item': next_generation_data[index],
#                'fitness': next_generation_fitness[index],
#            })
#
#        result_data['generations'].append(generation_data)
#        # result_data['generations_fitness'].append(next_generation_fitness)
#        result_data['generations_best_item'].append(best_item)
#        result_data['generations_best_fitness'].append(best)
#        if not result_data['best'] or best > result_data['best']:
#            result_data['best'] = best
        # print(generation)
        # pprint.pprint(current_data)
#        current_data = next_generation_data
    result_data['generations'].append(fitness_vector(pareto_frontier))
    import pprint
    pprint.pprint(result_data)
    return result_data
