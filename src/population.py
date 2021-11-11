import random
import numpy as np

from individual import Individual
from fitness import calculate_fitness
from utils import array_of_ones_and_zeros

def create_random_individual(chromosome_length, rectangles,fitness_fuction, seed):
    # solo usarlo cuando se quiere hacer debug
    # np.random.seed(seed)
    # chromosome_length is an array e.g: [0,1,2,3,4,5,6,7,8,9]
    gene_list = np.random.permutation(chromosome_length)
    #Array of ones and zeros randomly generated(second parameter is a seed)
    rotation_list = array_of_ones_and_zeros(len(chromosome_length),0)
    # A list of rectangles are passed down to each Individual to calculate its fitness
    return Individual(list(gene_list),rotation_list ,rectangles, fitness_fuction)

def create_starting_population(population_size, rectangles, genes,fitness_fuction):
    return np.array([create_random_individual(genes, rectangles, fitness_fuction, _) for _ in range(population_size)])





