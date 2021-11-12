import random
import numpy as np

from individual import Individual
from fitness import calculate_fitness
from utils import array_of_ones_and_zeros

def create_random_individual(genes, rectangles, fitness_fuction, it_rotates, seed):
    # only use seed for debugging
    # np.random.seed(seed)
    # genes is an array e.g: [0,1,2,3,4,5,6,7,8,9]
    gene_list = np.random.permutation(genes)
    #Array of ones and zeros randomly generated(second parameter is a seed)
    if it_rotates:
        rotation_list = array_of_ones_and_zeros(len(genes), 0)
    else:
        rotation_list =np.zeros(len(genes))
    # A list of rectangles are passed down to each Individual to calculate its fitness
    return Individual(list(gene_list),rotation_list ,rectangles, fitness_fuction,it_rotates)

def create_individual(genes, rectangles, fitness_fuction, it_rotates):
    # Array of ones and zeros randomly generated(second parameter is a seed)
    if it_rotates:
        rotation_list = array_of_ones_and_zeros(len(genes), 0)
    else:
        rotation_list = np.zeros(len(genes))
    # A list of rectangles are passed down to each Individual to calculate its fitness
    return Individual(list(genes), rotation_list, rectangles, fitness_fuction,it_rotates)

def create_starting_population(population_size, rectangles, genes, fitness_fuction, it_rotates):

    return np.array([create_random_individual(genes, rectangles, fitness_fuction,it_rotates,_) for _ in range(population_size)])





