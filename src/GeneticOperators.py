import random
# from numpy.random import choice
import numpy as np


# MUTATION OPERATORS
def reverse_sequence_mutation(offspring, mutation_probability):
    """
     The RSM method chooses two random points in the chromosome and selects the section of genes in between. The gene
     sequence inside the selected section is then reversed
     Source: https://www.researchgate.net/publication/345339544_A_Comparison_of_GA_Crossover_and_Mutation_Methods_for_the_Traveling_Salesman_Problem#pfe

    :param mutation_probability:
    :param offspring: Offspring to mutate
    :return: Mutated offspring with a probability of mutation_probability
    """
    r_pm = random.random()
    # To ensure that the mutation operator is only applied with a probability of mutation_probability
    if r_pm >= mutation_probability:
        return offspring

    # I create a new shallow copied list so that I don't affect the existing chromosome (no in place changes)
    mutated_offspring = list(offspring)

    idx1 = random.randint(0, len(offspring) - 2)
    idx2 = random.randint(idx1 + 1, len(offspring) - 1)

    middle = offspring[idx1: idx2 + 1]

    mutated_offspring[idx1: idx2 + 1] = middle[::-1]

    return mutated_offspring


def twors_mutation(offspring, mutation_probability):
    """
    As our chromosome is encoded as a list of indices, we mutate by swapping two positions.
    Twors mutation: https://arxiv.org/ftp/arxiv/papers/1203/1203.3099.pdf

    :param mutation_probability:
    :param offspring: Offspring to mutate
    :return: Mutated offspring with a probability of mutation_probability
    """
    r_pm = random.random()
    # To ensure that the mutation operator is only applied with a probability of mutation_probability
    if r_pm >= mutation_probability:
        return offspring

    idx1 = random.randint(0, len(offspring) - 1)
    idx2 = -1
    # To ensure idx1 and idx2 are not the same
    while idx1 == idx2:
        idx2 = random.randint(0, len(offspring) - 1)

    # This is shallow copy and it works in our case
    mutated_offspring = list(offspring)
    # Swap indices
    temp = offspring[idx1]
    mutated_offspring[idx1] = offspring[idx2]
    mutated_offspring[idx2] = temp

    return mutated_offspring


def centre_inverse_mutation(offspring, mutation_probability):
    """
    This applies the Centre Inverse Mutation. We pick a random point to divide the chromosome into two sections.
    Then, the two sections are flipped.
    https://www.researchgate.net/publication/345339544_A_Comparison_of_GA_Crossover_and_Mutation_Methods_for_the_Traveling_Salesman_Problem#pfe


    :param mutation_probability:
    :param offspring: Offspring to be mutated
    :return: Mutated offspring
    """
    r_pm = random.random()
    # To ensure that the mutation operator is only applied with a probability of mutation_probability
    if r_pm >= mutation_probability:
        return offspring

    # Shallow copy
    mutated_offspring = list(offspring)

    split_idx = random.randint(0, len(offspring) - 1)
    left = offspring[:split_idx]
    right = offspring[split_idx:]

    # [::-1] flips the list
    mutated_offspring[:split_idx] = left[::-1]
    mutated_offspring[split_idx:] = right[::-1]

    return mutated_offspring


# CROSSOVER OPERATORS

def ordered_crossover(parent1, parent2, cross_over_probability):
    """
    This is an ordered crossover operator.

    :param cross_over_probability: Apply the operator with a probability of this
    :param parent1: It is the first parent
    :param parent2: It is the second parent
    :return: Returns the two offspring after applying the crossover operator
    """

    r_pc = random.random()
    # To ensure that the crossover operator is only applied with a probability of cross_over_probability
    if r_pc >= cross_over_probability:
        return parent1, parent2

    subset_size = random.randint(1, len(parent1) - 1)
    left_split = random.randint(0, len(parent1) - subset_size)
    right_split = left_split + subset_size

    middle_part1 = parent1[left_split: right_split]
    middle_part2 = parent2[left_split: right_split]

    offspring1 = [-1] * len(parent1)
    offspring2 = [-1] * len(parent2)

    # Set the middle part same as the parent
    offspring1[left_split: right_split] = middle_part1
    offspring2[left_split: right_split] = middle_part2

    # Fill the remaining part of the offspring genes from the other parent while preserving the order
    for i in range(len(parent1)):
        if parent2[i] not in middle_part1:
            for j in range(len(parent1)):
                if offspring1[j] == -1:
                    offspring1[j] = parent2[i]
                    break
        if parent1[i] not in middle_part2:
            for j in range(len(parent2)):
                if offspring2[j] == -1:
                    offspring2[j] = parent1[i]
                    break

    return offspring1, offspring2


# SELECTION OPERATORS

def roulette_selection(tsp_data, population):
    """
    Uses the roulette selection method for selection.

    Each chromosome in the population is assigned a probability of selection based on its fitness value relative
    to the other chromosomes. The fitter chromosomes are assigned a higher probability of selection, so they are
    more likely to be chosen as parents for the next generation.

    :param tsp_data: Data
    :param population: Fitness of all the chromosomes in the population
    :return: Returns indices of two from the population based on the probability (fitness ratio)
    """
    fitness_population = [fitness(tsp_data, chromosome) for chromosome in population]
    fitness_sum = sum(fitness_population)
    fitness_ratio = [fitness_chromosome / fitness_sum for fitness_chromosome in fitness_population]
    return int(np.random.choice(a=[*range(len(fitness_population))], size=1, replace=False, p=fitness_ratio))


def tournament_selection_with_pool_size(pool_size):
    """
    It returns a function closure. I used this to make sure that we are able to use pool_size while keeping
    function signature same as roulette_selection

    :param pool_size: size of the pool. Ensure that it is less than population size
    :return:
    """

    def tournament_selection(tsp_data, population):
        pool = np.random.choice(a=[*range(len(population))], size=pool_size, replace=False)  # Gets indices
        idx = pick_with_best_fitness(tsp_data, [population[i] for i in pool])
        return idx

    return tournament_selection


def rank_based_selection(tsp_data, population):
    fitness_population = [fitness(tsp_data, chromosome) for chromosome in population]
    # Creates a rank list
    indices = list(range(len(fitness_population)))
    indices.sort(key=lambda a: fitness_population[a])
    rank = [0] * len(indices)
    for i, x in enumerate(indices):
        rank[x] = i + 1
    sum_rank = (len(rank)) * (len(rank) + 1) / 2
    rank_prob = [rank[i] / sum_rank for i in range(len(rank))]
    # Normalised rank prob to avoid "sum not to 1 error"
    n_rank_prob = [rank_prob[i] / sum(rank_prob) for i in range(len(rank_prob))]
    return int(np.random.choice(a=[*range(len(fitness_population))], size=1, replace=False, p=n_rank_prob))


# OTHER HELPER FUNCTIONS
def pick_with_best_fitness(tsp_data, population):
    """

    :param tsp_data: Data with distance
    :param population: A list of chromosomes
    :return: The index of the product with the highest fitness
    """
    fitness_values = [fitness(tsp_data, chromosome) for chromosome in population]
    return np.array(fitness_values).argmax()


def pick_top_n_fitness(tsp_data, population, n):
    fitness_values = [fitness(tsp_data, chromosome) for chromosome in population]
    np_fitness = np.array(fitness_values)
    # Reverses the array first because argsort is ascending
    return np.argsort(np_fitness)[::-1][:n]


def fitness(tsp_data, chromosome):
    """
    Computes the fitness function for a given chromosome. The fitness is the inverse of length of the route.
    We need to minimise the length, so we take the inverse.

    :param tsp_data: Data of product distances
    :param chromosome: A particular order in which products can be taken. A possible solution
    :return: An integer representing the distance or the length of the route
    """

    distance = compute_total_route_length(tsp_data, chromosome)

    return 1 / distance


def compute_total_route_length(tsp_data, chromosome):
    distance = 0
    distance += tsp_data.get_start_distances()[
        chromosome[0]]  # Adds the distance from the start point to the first product
    prev_product = chromosome[0]

    for i in range(1, len(chromosome)):
        current_product = chromosome[i]
        distance += tsp_data.get_distances()[prev_product][current_product]
        prev_product = current_product

    distance += tsp_data.get_end_distances()[prev_product]

    return distance
