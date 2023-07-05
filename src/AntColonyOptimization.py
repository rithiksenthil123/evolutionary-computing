import sys
import time
from Maze import Maze
from PathSpecification import PathSpecification
from Ant import Ant

# Class representing the first assignment. Finds shortest path between two points in a maze according to a specific
# path specification.
class AntColonyOptimization:

    # Constructs a new optimization object using ants.
    # @param maze the maze .
    # @param antsPerGen the amount of ants per generation.
    # @param generations the amount of generations.
    # @param Q normalization factor for the amount of dropped pheromone
    # @param evaporation the evaporation factor.
    def __init__(self, maze, ants_per_gen, generations, q, e, evaporation, alpha, beta, convergence_length, max_step, max_step_once_found):
        self.maze = maze
        self.ants_per_gen = ants_per_gen
        self.generations = generations
        self.q = q
        self.e = e
        self.evaporation = evaporation
        self.alpha = alpha
        self.beta = beta
        self.convergence_length = convergence_length
        self.max_step = max_step
        self.max_step_once_found = max_step_once_found

     # Loop that starts the shortest path process
     # @param spec Spefication of the route we wish to optimize
     # @return ACO optimized route
    def find_shortest_route(self, path_specification):

        # Reset the maze for the new shortest route problem
        self.maze.reset()
        global_shortest = None
        shortest_each_gen = []

        for gen in range(self.generations):
            print("Releasing generation", gen+1)

            shortest_this_gen = None

            # Release new generation of ants and let them find their routes
            routes = []
            for i in range(self.ants_per_gen):
                print('Releasing Ant:', i)
                curr_route = Ant(self.maze, path_specification).find_route(self.alpha, self.beta, self.max_step)
                routes.append(curr_route)

            # Update the shortest route
            for i in range(self.ants_per_gen):
                if (global_shortest is None or (routes[i] is not None and routes[i].shorter_than(global_shortest))):
                    global_shortest = routes[i]
                if (shortest_this_gen is None or (routes[i] is not None and routes[i].shorter_than(shortest_this_gen))):
                    shortest_this_gen = routes[i]

            # Check convergence criterion
            if (global_shortest is not None and global_shortest.size() <= self.convergence_length):
                break

            if (shortest_this_gen is None):
                shortest_each_gen.append(sys.maxsize)
            else:
                self.max_step = self.max_step_once_found
                shortest_each_gen.append(shortest_this_gen.size())

            # Update pheromones based on evaporation constant and found routes
            self.maze.evaporate(self.evaporation)
            self.maze.add_pheromone_routes(routes, self.q)
            # Enforce elitism by adding additional pheromone to the global best route (simulate e specialist ants)
            self.maze.add_pheromone_route(global_shortest, self.q * self.e)

        return global_shortest, shortest_each_gen