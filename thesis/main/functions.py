"""Contain the functions for main app."""

import json
import pprint

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
        data = generate_init_data(10, 3)
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


def fitness(data):
    """Fitness function."""
    return sum(item for item in data)


def evaluate_fitness(data, crossover_data):
    """Get the next generation children using fitness function."""
    next_generation_data = []
    best = None
    for index, item in enumerate(data):
        data_fitness = fitness(data[index])
        crossover_fitness = fitness(crossover_data[index])
        if data_fitness > crossover_fitness:
            best_fitness = data_fitness
            next_genetation_item = data[index]
        else:
            best_fitness = crossover_fitness
            next_genetation_item = crossover_data[index]

        if not best or best_fitness > best:
            best = best_fitness
        next_generation_data.append(next_genetation_item)
    return next_generation_data, best

def differential_evolution(generations, data):
    """Apply differential evolution on a dataset."""
    result_data = {
        'generations_best': [],
        'best': None,
    }
    current_data = data

    for generation in range(generations):
        mutate_data = get_mutate_data(current_data)
        crossover_data = get_crossover_data(current_data, mutate_data)
        next_generation_data, best = evaluate_fitness(current_data, crossover_data)
        result_data['generations_best'].append(best)
        if not result_data['best'] or best > result_data['best']:
            result_data['best'] = best
        current_data = next_generation_data
    return result_data
