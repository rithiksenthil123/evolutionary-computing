import random
from Route import Route
from Direction import Direction
from SurroundingPheromone import SurroundingPheromone
from Maze import Maze


# Class that represents the ants functionality.
class Ant:

    # Constructor for ant taking a Maze and PathSpecification.
    # @param maze Maze the ant will be running in.
    # @param spec The path specification consisting of a start coordinate and an end coordinate.
    def __init__(self, maze, path_specification):
        self.maze = maze
        self.start = path_specification.get_start()
        self.end = path_specification.get_end()
        self.current_position = self.start
        self.rand = random

    # Method that performs a single run through the maze by the ant.
    # @return The route the ant found through the maze.
    def find_route(self, alpha, beta, max_step):
        route = Route(self.start)
        found_end = False
        dir_to_previous_pos = None
        old_location = self.start
        dead_end_path = []
        positions = [self.start]

        for i in range(max_step):
            # Get the surrounding pheromone in format of a list (E,N,W,S)
            surrounding_pheromone = self.maze.get_surrounding_pheromone(self.current_position)

            # Exclude direction from which the ant came
            if (dir_to_previous_pos is not None):
                surrounding_pheromone[dir_to_previous_pos] = 0

            # Calculate the possible directions
            path_opportunities = 0
            for pheromone in surrounding_pheromone:
                if pheromone > 0:
                    path_opportunities += 1

            # Multiple path opportunities
            if path_opportunities == 2 or path_opportunities == 3 or path_opportunities == 4:
                # Restart dead end counter
                dead_end_path = []
                old_location = self.current_position

                # Compute probability of choosing for each direction
                total_pheromone = 0
                for t in surrounding_pheromone:
                    total_pheromone += (t**alpha) * (1**beta)
                for i in range(len(surrounding_pheromone)):
                    surrounding_pheromone[i] = (surrounding_pheromone[i]**alpha) * (1**beta) / total_pheromone

                # Get a random direction based on computed probabilities
                directions = [Direction.east, Direction.north, Direction.west, Direction.south]
                direction = self.rand.choices(directions, k=1, weights=surrounding_pheromone)
                direction = direction[0]
                dir_to_previous_pos = Direction.opposite(direction)

                route.add(direction)
                self.current_position = self.current_position.add_direction(direction)

            # Only one path possible
            if path_opportunities == 1:
                # If a one way street walks past the start location, it resets the dead end counter
                if self.current_position == self.start:
                    dead_end_path = []
                    old_location = self.current_position
                else:
                    dead_end_path.append(self.current_position)
                # Compute probability of choosing for each direction
                total_pheromone = 0
                for t in surrounding_pheromone:
                    total_pheromone += (t**alpha) * (1**beta)
                for i in range(len(surrounding_pheromone)):
                    surrounding_pheromone[i] = (surrounding_pheromone[i]**alpha) * (1**beta) / total_pheromone

                # Get a random direction based on computed probabilities
                directions = [Direction.east, Direction.north, Direction.west, Direction.south]
                direction = self.rand.choices(directions, k=1, weights=surrounding_pheromone)
                direction = direction[0]
                dir_to_previous_pos = Direction.opposite(direction)

                route.add(direction)
                self.current_position = self.current_position.add_direction(direction)

            # Dead end
            if path_opportunities == 0:
                # Check if dead end is the start and reset the dead end counter
                if self.current_position == self.start:
                    dead_end_path = []
                    old_location = self.current_position
                # If not start change the maze and set the dead end paths to pheromone value 0
                else:
                    # Check if dead end is the end, if it is it will not remove anything from route
                    if self.current_position == self.end:
                        break
                    dead_end_path.append(self.current_position)
                    for dead_path in dead_end_path:
                        self.maze.change_pheromone(dead_path, 0)
                    for x in range(len(dead_end_path) - 1):
                        route.remove_last()
                    dead_end_path = []
                    self.current_position = old_location
            # Check if the end was reached
            if self.current_position == self.end:
                print("The ant found the end location")
                found_end = True
                break

            for i in range(len(positions)):
                if (self.current_position == positions[i]):
                    positions = positions[:i]
                    route.route = route.route[:i]
                    if len(route.route) > 0:
                        dir_to_previous_pos = Direction.opposite(route.route[-1])
                    else:
                        dir_to_previous_pos = None
                    break
            positions.append(self.current_position)

        if found_end:
            return route
        return None
