# Supermarket Navigation with Swarm Intelligence

This project focuses on enabling a robot to navigate efficiently in a supermarket to find multiple products. The supermarket is represented as a labyrinth or maze, and the robot's objective is to determine the fastest route to visit a set of predefined locations within the supermarket. To solve this problem, two techniques are employed: the Traveling Salesman Problem (TSP) using a Genetic Algorithm and path finding based on Ant Colony Optimization (ACO) using Swarm Intelligence.

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
  
## Overview

This project tackles the challenge of optimizing navigation in a supermarket environment by efficiently finding the fastest route to visit multiple locations. It leverages two distinct techniques to achieve this goal: 

1. **Traveling Salesman Problem (TSP)**: The TSP aspect of the project addresses the problem of finding the shortest possible route that visits a set of locations exactly once and returns to the starting point. This is achieved through the implementation of a Genetic Algorithm, which evolves a population of potential solutions to iteratively improve the fitness of the routes.

2. **Ant Colony Optimization (ACO) based Path Finding**: The path finding aspect of the project is based on Ant Colony Optimization, a metaheuristic algorithm inspired by the behavior of ants when searching for the shortest path between their colony and a food source. The ACO algorithm simulates the movement of virtual ants, depositing pheromone trails on the paths they traverse. These trails attract other ants, enabling the discovery of efficient routes in the maze.

## Installation

To run this project locally, follow the steps below:

1. Clone the repository to your local machine using the following command:

```bash
git clone https://github.com/your-username/your-repo.git
```

2. Install the necessary dependencies by navigating to the project directory and running the following command:

```bash
pip install -r requirements.txt
```

3. Set up any additional configurations or parameters as required for your specific supermarket environment.

## Usage

This project consists of two main components: TSP and ACO path finding. Here's an overview of how to use each component:

### TSP (Traveling Salesman Problem)

1. Open the TSP module and provide the locations you want to visit within the supermarket.
2. Adjust any TSP-specific parameters or configurations, such as population size, mutation rate, and number of generations.
3. Run the TSP algorithm to find the optimal route that visits all locations once and returns to the starting point.
4. Analyze the output to determine the fastest route for your robot to follow.

### ACO (Ant Colony Optimization) Path Finding

1. Configure the supermarket maze environment by providing the layout, obstacles, and target locations.
2. Adjust ACO-specific parameters, such as the number of ants, pheromone evaporation rate, and convergence criteria.
3. Run the ACO algorithm to allow virtual ants to find efficient paths between the target locations within the maze.
4. Analyze the output to obtain the optimized path for your robot to follow.

Feel free to modify the code and experiment with different parameters to suit your specific supermarket environment and requirements.

## Contributing

Contributions to this project are welcome and appreciated! If you wish to contribute, please follow these steps:

1. Fork the repository on GitHub.
2. Create a new branch with a descriptive name for your feature or bug fix.
3. Implement your changes, documenting and testing them as necessary.
4. Submit a pull request, providing a clear explanation of your modifications and their benefits.
---

With the Supermarket Navigation project, you can optimize the navigation of your robot in a supermarket maze by determining the fastest route to visit multiple locations. The combination of TSP and ACO techniques allows for efficient path planning and navigation. If you have any questions or suggestions, please feel free to reach out and contribute to the project.

Happy navigating!
