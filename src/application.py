import random
import numpy as np

from rectangle import generate_N_ractangles
from selection import select_tournament
from crossover import crossover
from mutate import mutate
from population import create_starting_population
from fitness import calculate_fitness
from utils import generate_stack_of_strips_NFDH, get_best_individual, get_average_fitness, calculate_best_individual_values_NFDH
from plotting import plot_result, plot_rectangles

from GLOBAL import W, POPULATION_SIZE, MAX_GENERATIONS, MUTATION_PROBABILITY, \
    CROSS_OVER_PROBABILITY,TOURNAMENT_SIZE,RECTANGLES_NUMBER


def GA(number_of_rectangles, genes):
    solutions = []
    best_individuals = []
    best_fitness_acc = []
    average_fitness_acc = []

    # Generate reference rectangle list
    set_of_rectangles = generate_rectangles(number_of_rectangles)

    # Start inicial population
    population = create_starting_population(POPULATION_SIZE, set_of_rectangles, genes)

    # Calculates the best and average for que starting population
    best_initial_individual = get_best_individual(population)
    average_fitness = get_average_fitness(population)
    stack = generate_stack_of_strips_NFDH(best_initial_individual.get_gene_list(), set_of_rectangles, W)

    print("-------RECTANGLES----------")
    for rec in set_of_rectangles:
        print(rec)

    print("-----------------------------------------------------")
    print("Best Initial individual: ", best_initial_individual.gene_list)
    print("Best Initial Fitness: ", best_initial_individual.fitness)
    print("Initial population Average fitness: ", average_fitness)
    print("Solution: ", stack)
    print("-----------------------------------------------------")
    plot_rectangles(set_of_rectangles, stack, best_initial_individual.gene_list, best_initial_individual.fitness, "initial", W,
                    FOLDER_NFDH)

    for generation_number in range(MAX_GENERATIONS):

        # SELECTION
        selected = select_tournament(population, TOURNAMENT_SIZE)

        # CROSSOVER
        crossed_offspring = []

        for ind1, ind2 in zip(selected[::2], selected[1::2]):
            # random.seed(1)
            if random.random() < CROSS_OVER_PROBABILITY:
                children = crossover(ind1.gene_list, ind2.gene_list, set_of_rectangles, calculate_fitness)
                crossed_offspring.append(children[0])
                crossed_offspring.append(children[1])
            else:
                crossed_offspring.append(ind1)
                crossed_offspring.append(ind2)
        # MUTATION
        mutated = []
        for ind in crossed_offspring:
            # random.seed(1)
            if random.random() < MUTATION_PROBABILITY:
                mutated.append(mutate(ind.gene_list, set_of_rectangles, number_of_rectangles, calculate_fitness))
            else:
                mutated.append(ind)

        population = mutated

        best_genes, best_fitness, average_fitness, stack_of_strips, best_genes = calculate_best_individual_values_NFDH(population, set_of_rectangles)

        best_individuals.append(best_genes)
        best_fitness_acc.append(best_fitness)

        # averagen fitness
        average_fitness_acc.append(average_fitness)
        #solution
        solutions.append(stack_of_strips)


    plot_result(average_fitness_acc,MAX_GENERATIONS, FOLDER_NFDH, "Average fitness")
    plot_result(best_fitness_acc, MAX_GENERATIONS, FOLDER_NFDH, "Best fitness")

    for j in range(MAX_GENERATIONS):
        print(" -- ")
        print("Generation: ", j)
        print("Best individual: ", best_individuals[j])
        print("Solution: ", solutions[j])
        print("Fitness: ", best_fitness_acc[j])

    # Print and save the plots
    #if MAX_GENERATIONS <= 1000:
   # for c in range(MAX_GENERATIONS):
    #    plot_rectangles(set_of_rectangles, solutions[c], best_individuals[c], best_fitness_acc[c], c, W, FOLDER_NFDH)

if __name__ == '__main__':
    data = [(37,11),(26,68),(25,75),(24,17),(20,73),(30,28),(12,35),(25,47)]
    rectangles = generate_N_ractangles(len(data),data)

    population = create_starting_population(POPULATION_SIZE, rectangles, np.arange(len(data)),calculate_fitness)
    for p in population:
        print(p)
