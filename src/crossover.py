import random
from math import nan
from population import create_individual
import copy


def order_crossover(p1, p2, seed):

    random.seed(seed)
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


def crossover_one_point(p1, p2,seed):
    random.seed(seed)
    point = random.randint(1, len(p1) - 1)
    c1, c2 = copy.deepcopy(p1), copy.deepcopy(p2)
    c1[point:], c2[point:] = p2[point:], p1[point:]
    return [c1, c2]


def crossover(ind1, ind2, max_width, rectangles, fitness_function, seed, it_rotates):

    offspring_genes = order_crossover(ind1.gene_list, ind2.gene_list, seed)
    offspring_rotation = crossover_one_point(ind1.rotation, ind2.rotation, seed)

    return[create_individual(offspring_genes[0], offspring_rotation[0], max_width, rectangles, fitness_function, seed, it_rotates),
           create_individual(offspring_genes[1], offspring_rotation[1],  max_width, rectangles, fitness_function, seed, it_rotates)]

