import random
import sys

import numpy as np
from TSPData import TSPData
import matplotlib.pyplot as plt
from GeneticOperators import pick_with_best_fitness, pick_top_n_fitness, compute_total_route_length, fitness


# TSP problem solver using genetic algorithms.
class GeneticAlgorithm:

    # Constructs a new 'genetic algorithm' object.
    # @param generations the amount of generations.
    # @param popSize the population size.
    def __init__(self, generations, pop_size, crossover_operator, mutation_operator, selection_method,
                 mutation_probability=0.01, cross_over_probability=0.7, elitism=0):
        self.selection_method = selection_method
        self.elitism = elitism
        self.crossover_operator = crossover_operator
        self.mutation_operator = mutation_operator
        self.generations = generations
        self.pop_size = pop_size
        self.mutation_probability = mutation_probability
        self.cross_over_probability = cross_over_probability

    # This method should solve the TSP.
    # @param pd the TSP data.
    # @return the optimized product sequence.
    def solve_tsp(self, tsp_data):
        # Initialise the population randomly
        current_gen = [self.generate_chromosome(tsp_data) for _ in
                       range(self.pop_size)]  # Randomly create the first generation
        idk = 0
        prev = sys.maxsize
        best_distance_per_gen = []

        for gen_i in range(self.generations):
            print("In generation {}...".format(gen_i + 1))

            next_gen = []

            if self.elitism > 0:
                indices_of_parent = pick_top_n_fitness(tsp_data, current_gen, self.elitism)
                for idx in indices_of_parent:
                    next_gen.append(current_gen[idx])
            while len(next_gen) < self.pop_size:
                idx_of_parent1 = self.selection_method(tsp_data, current_gen)
                idx_of_parent2 = self.selection_method(tsp_data, current_gen)
                offspring1, offspring2 = self.crossover_operator(current_gen[idx_of_parent1],
                                                                 current_gen[idx_of_parent2],
                                                                 self.cross_over_probability)
                offspring1 = self.mutation_operator(offspring1, self.mutation_probability)
                offspring2 = self.mutation_operator(offspring2, self.mutation_probability)

                next_gen.append(offspring1)
                next_gen.append(offspring2)

            # Print details about the gen before running the operators
            best_solution = pick_with_best_fitness(tsp_data, next_gen)
            best_distance_per_gen.append(compute_total_route_length(tsp_data, next_gen[best_solution]))
            prev = best_distance_per_gen[idk]
            idk += 1
            current_gen = next_gen
            print(
                "Best solution in generation {} is the chromosome {} with a fitness ratio of {} and distance of {}\n".
                format(gen_i + 1, next_gen[best_solution], fitness(tsp_data, next_gen[best_solution]),
                       compute_total_route_length(tsp_data, next_gen[best_solution]))
            )

        fitness_for_last_gen = [fitness(tsp_data, gen) for gen in current_gen]
        best_solution = pick_with_best_fitness(tsp_data, current_gen)

        # Plot the generation vs distance graph
        plt.plot([*range(1, self.generations + 1)], best_distance_per_gen)
        plt.title("Best route each generation\nMutation Operator: {}\nCrossover Operator: {}\nSelection Method: {}"
                  .format(self.mutation_operator.__name__, self.crossover_operator.__name__,
                          self.selection_method.__name__))
        plt.ylabel("Shortest Route Length")
        plt.ylim([1200, 6000])
        plt.xlabel("Generation")
        plt.show()

        # return current_gen[best_solution], fitness_for_last_gen[best_solution], self.compute_total_route_length(
        #     tsp_data, current_gen[best_solution])
        return current_gen[best_solution]



    def generate_chromosome(self, tsp_data):
        """
        Chromosome encoding -> A list of indices (starting from 0) of products. It is a possible solution. It is the order in which the
        products can be collected.

        :param tsp_data: the data with product distance data
        :return: returns a randomly generated chromosome
        """
        product_indices = [*range(len(tsp_data.product_locations))]
        return random.sample(product_indices, k=len(product_indices))
