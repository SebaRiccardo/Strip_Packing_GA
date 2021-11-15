
from population import create_individual
import numpy as np


def mutate(genes, max_width, rectangles, rectangles_number, fitness_function, seed, it_rotates):
    np.random.seed(seed)
    indexA = 0
    indexB = 0

    # checks if the indexes are the same
    while indexA == indexB:
        indexA = np.random.randint(0, rectangles_number)
        indexB = np.random.randint(0, rectangles_number)

    # swap values at indexA and indexB A y B
    newGenes = np.copy(genes)
    geneA = newGenes[indexA]
    newGenes[indexA] = newGenes[indexB]
    newGenes[indexB] = geneA
    return create_individual(newGenes, max_width,rectangles, fitness_function, seed, it_rotates)

