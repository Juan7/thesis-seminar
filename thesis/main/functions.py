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


def mutate_element(index, item, data):
    """Mutate an elemtn on a dataset."""
    taken_indexes = [index]
    index_0 = get_random_diff_than(taken_indexes, data)
    index_1 = get_random_diff_than(taken_indexes, data)
    index_2 = get_random_diff_than(taken_indexes, data)

    mutate_vector = sum_array(
                        data[index_0],
                        scalar_multiply_array(settings.SCALE_FACTOR, substract_array(data[index_1],data[index_2])))
    return mutate_vector


def get_mutate_data(data):
    """Get mutate data according on differential evolution method."""
    mutate_data = []
    for index, item in enumerate(data):
        mutate_vector = mutate_element(index, item, data)
        mutate_data.append(mutate_vector)
    return mutate_data


def crossover_elements(element_1, element_2):
    """Crossover two elements."""
    crossover_element = []
    for index, item in enumerate(element_1):
        mutate_item = element_1[index] if random() < settings.CROSSOVER_RATE else element_2[index]
        crossover_element.append(mutate_item)
    return crossover_element


def get_crossover_data(data, mutate_data):
    """Get crossover data."""
    crossover_data = []
    for index, item in enumerate(data):
        crossover_vector = crossover_elements(data[index], mutate_data[index])
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
        return False

def total_dominate(item_1_data, item_1_results, item_2_data, item_2_results, index, crossover_data):
    """Force the domination disturbing item."""
    dominator = dominate(item_1_data, item_1_results, item_2_data, item_2_results)
    while not dominator:
        mutate_item = mutate_element(index, item_2_data['item'], crossover_data)
        crossover_item = crossover_elements(item_2_data['item'], mutate_item)
        crossover_item_results = evaluate_multi_fitness(crossover_item)
        crossover_item_data = {'item': crossover_item, 'fitness': crossover_item_results}
        dominator = dominate(item_1_data, item_1_results, crossover_item_data, crossover_item_results)
    return dominator

def pareto_optimal(item_1, item_2, index, crossover_data):
    """Check what element dominates."""
    item_1_results = evaluate_multi_fitness(item_1)
    item_2_results = evaluate_multi_fitness(item_2)

    item_1_data = {'item': item_1, 'fitness': item_1_results}
    item_2_data = {'item': item_2, 'fitness': item_2_results}

    return total_dominate(item_1_data, item_1_results, item_2_data, item_2_results, index, crossover_data)


def pareto_compares(item_1, item_2):
    """Return the compares between 2 arrays."""
    return item_1[0] > item_2[0] and item_1[1] < item_2[1]

def sum_fitness(data):
    """Fitness function."""
    return sum(item for item in data)


def minus_fitness(data):
    """Fitness function."""
    diff = 0
    for item in data:
        diff -= item
    return diff


def evaluate_fitness(data, crossover_data):
    """Get the next generation children using fitness function."""
    next_generation_data = []
    for index, item in enumerate(data):
        current_generation_data = pareto_optimal(data[index], crossover_data[index], index, crossover_data)
        next_generation_data.append(current_generation_data)
    return next_generation_data


def one_dominates_two(item_1_data, item_2_data):
    """Check if first dominate second."""
    return (item_1_data['fitness'][0] > item_2_data['fitness'][0]
            and item_1_data['fitness'][1] < item_2_data['fitness'][1])


def pareto_dominance(item, data):
    """Check if an item has another who dominates it."""
    for current_item in data:
        if one_dominates_two(current_item, item)

def calculate_pareto_frontier(generation_data, result_data):
    """Remove the dominated items."""
    index = 0
    for target_index, generation_item in enumerate(generation_data):


    if not any(one_dominates_two(pareto_item, generation_item) for pareto_item in result_data['pareto_frontier'])
        result_data['pareto_frontier'].append(generation_item)



def differential_evolution(generations, data):
    """Apply differential evolution on a dataset."""
    result_data = {
        # 'generations_best_item': [],
        # 'generations_best_fitness': [],
        'generations': [],
        'pareto_frontier': [],
        # 'generations_fitness': [],
        'best': None,
    }
    current_data = data
    init_generation_data = []
    for current_item in current_data:
        current_item_results = evaluate_multi_fitness(current_item)
        current_item_data = {'item': current_item, 'fitness': current_item_results}
        init_generation_data.append(current_item_data)

    calculate_pareto_frontier(init_generation_data, result_data)
    for generation in range(generations):
        mutate_data = get_mutate_data(current_data)
        crossover_data = get_crossover_data(current_data, mutate_data)
        generation_data = evaluate_fitness(current_data, crossover_data)

        next_generation_data = []
        for index, item in enumerate(next_generation_data):
            next_generation_data.append(next_generation_data['item'])



        current_data = next_generation_data
    return result_data
