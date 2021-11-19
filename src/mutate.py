
from population import create_individual
import numpy as np


def mutate(genes, rotation, max_width, rectangles, rectangles_number, fitness_function, seed, it_rotates):
    np.random.seed(seed)
    index_a = np.random.randint(0, rectangles_number)
    index_b = np.random.randint(0, rectangles_number)

    # checks if the indexes are the same
    while index_a == index_b:
        index_a = np.random.randint(0, rectangles_number)
        index_b = np.random.randint(0, rectangles_number)

    # swap values at indexA and indexB A y B
    new_genes = np.copy(genes)
    gene_a = new_genes[index_a]
    new_genes[index_a] = new_genes[index_b]
    new_genes[index_b] = gene_a
    return create_individual(new_genes, rotation, max_width, rectangles, fitness_function, seed, it_rotates)

