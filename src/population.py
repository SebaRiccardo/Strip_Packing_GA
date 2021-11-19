import random
import numpy as np

from individual import Individual
from fitness import calculate_fitness
from utils import array_of_ones_and_zeros

# -------- fun for generating starting population --------- #
def generate_rotation_list(genes, it_rotates, seed):
    if it_rotates:
        rotation_list = array_of_ones_and_zeros(len(genes), seed)
    else:
        rotation_list = list(np.zeros(len(genes)).astype(int))
    return rotation_list

#creates a random individual this function is used to create random individual with a random list of genes.
def create_random_individual(genes, max_width, rectangles, fitness_fuction, it_rotates, seed):
    # only use seed for debugging
    np.random.seed(seed)
    # genes is an array e.g: [0,1,2,3,4,5,6,7,8,9]
    permuted_list = np.random.permutation(genes)
    # Array of ones and zeros randomly generated(second parameter is a seed)
    rotation_list = generate_rotation_list(genes,it_rotates,seed)

    # A list of rectangles are passed down to each Individual to calculate its fitness
    return Individual(list(permuted_list),rotation_list, max_width, rectangles, fitness_fuction, it_rotates)

#creates the starting  random population
def create_starting_population(population_size, max_width, rectangles, genes, fitness_fuction, it_rotates,seed):
    return np.array([create_random_individual(genes, max_width, rectangles, fitness_fuction,it_rotates,_ + seed) for _ in range(population_size)])
#-----------------<================>----------------#


def create_individual(genes, rotation, max_width, rectangles, fitness_fuction, seed, it_rotates):
    # A list of rectangles are passed down to each Individual to calculate its fitness
    return Individual(list(genes), rotation, max_width, rectangles, fitness_fuction, it_rotates)

