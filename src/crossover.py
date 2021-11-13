import random
from math import nan
from GLOBAL import SEED
import numpy as np

from population import create_individual


def crossover_order(p1, p2):
    #random.seed(SEED)
    zero_shift = min(p1)
    length = len(p1)
    start, end = sorted([random.randrange(length) for _ in range(2)])
    c1, c2 = [nan] * length, [nan] * length
    t1, t2 = [x - zero_shift for x in p1], [x - zero_shift for x in p2]

    spaces1, spaces2 = [True] * length, [True] * length
    for i in range(length):
        if i < start or i > end:
            spaces1[t2[i]] = False
            spaces2[t1[i]] = False

    j1, j2 = end + 1, end + 1
    for i in range(length):
        if not spaces1[t1[(end + i + 1) % length]]:
            c1[j1 % length] = t1[(end + i + 1) % length]
            j1 += 1

        if not spaces2[t2[(i + end + 1) % length]]:
            c2[j2 % length] = t2[(i + end + 1) % length]
            j2 += 1

    for i in range(start, end + 1):
        c1[i], c2[i] = t2[i], t1[i]

    return [[x + zero_shift for x in c1], [x + zero_shift for x in c2]]


def crossover(genes_ind1, genes_ind2, max_width, rectangles, fitness_function, it_rotates):

    offspring_genes = crossover_order(genes_ind1, genes_ind2)
    return[create_individual(offspring_genes[0], max_width, rectangles, fitness_function, it_rotates),
           create_individual(offspring_genes[1], max_width, rectangles, fitness_function, it_rotates)]

