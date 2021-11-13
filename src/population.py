import random
import numpy as np

from individual import Individual
from fitness import calculate_fitness
from utils import array_of_ones_and_zeros

#creates a random individual this function is used to create random individual with a random list of genes.
def create_random_individual(genes, max_width, rectangles, fitness_fuction, it_rotates, seed):
    # only use seed for debugging
    #np.random.seed(seed)
    # genes is an array e.g: [0,1,2,3,4,5,6,7,8,9]
    permuted_list = np.random.permutation(genes)
    # Array of ones and zeros randomly generated(second parameter is a seed)
    if it_rotates:
        rotation_list = array_of_ones_and_zeros(len(genes), 0)
    else:
        rotation_list =np.zeros(len(genes))
    # A list of rectangles are passed down to each Individual to calculate its fitness
    return Individual(list(permuted_list),rotation_list, max_width, rectangles, fitness_fuction, it_rotates)

#creates the starting  random population
def create_starting_population(population_size, max_width, rectangles, genes, fitness_fuction, it_rotates,seed):


    population= np.array([create_random_individual(genes, max_width, rectangles, fitness_fuction,it_rotates,_ + seed) for _ in range(population_size)])

    return population
#creates a individual with a genes list. this function is used in mutation and crossover
def create_individual(genes, max_width, rectangles, fitness_fuction, it_rotates):
    # Array of ones and zeros randomly generated(second parameter is a seed)
    if it_rotates:
        rotation_list = array_of_ones_and_zeros(len(genes), 0)
    else:
        rotation_list = np.zeros(len(genes))
    # A list of rectangles are passed down to each Individual to calculate its fitness
    return Individual(list(genes), rotation_list, max_width, rectangles, fitness_fuction, it_rotates)



