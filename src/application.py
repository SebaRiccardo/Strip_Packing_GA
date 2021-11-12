import random
import numpy as np
from os import chdir
from rectangle import generate_N_ractangles
from selection import select_tournament
from crossover import crossover
from mutate import mutate
from population import create_starting_population
from fitness import calculate_fitness
from utils import generate_stack_of_strips, get_best_individual, get_average_fitness, calculate_best_individual_values
from plotting import plot_result, plot_rectangles

from GLOBAL import W, POPULATION_SIZE, MAX_GENERATIONS, MUTATION_PROBABILITY, \
    CROSS_OVER_PROBABILITY,TOURNAMENT_SIZE,RECTANGLES_NUMBER,RESULTS_FOLDER


def GA(number_of_rectangles, genes,it_rotates):
    solutions = []
    best_individuals = []
    best_fitness_acc = []
    average_fitness_acc = []
    rotations_acc =[]

    # Generate reference rectangle list
    set_of_rectangles = generate_rectangles(number_of_rectangles)

    # Start inicial population
    population = create_starting_population(POPULATION_SIZE, set_of_rectangles, genes,calculate_fitness,it_rotates)

    # Calculates the best and average for que starting population
    initial_best_genes, initial_best_fitness, initial_average_fitness, initial_stack_of_strips, initial_rotation = calculate_best_individual_values(population,set_of_rectangles,it_rotates)

    print("-------RECTANGLES----------")
    for rec in set_of_rectangles:
        print(rec)

    print("-----------------------------------------------------")
    print("Best Initial individual: ", initial_best_genes)
    print("Best Initial Fitness: ", initial_best_fitness)
    print("Rotation: ",initial_rotation)
    print("Initial population Average fitness: ", initial_average_fitness)
    print("Solution: ", initial_stack_of_strips)
    print("-----------------------------------------------------")
    plot_rectangles(set_of_rectangles, initial_stack_of_strips, initial_best_genes,initial_best_fitness, "initial", W, RESULTS_FOLDER,it_rotates)

    for generation_number in range(MAX_GENERATIONS):

        # SELECTION
        selected = select_tournament(population, TOURNAMENT_SIZE)

        # CROSSOVER
        crossed_offspring = []

        for ind1, ind2 in zip(selected[::2], selected[1::2]):
            # random.seed(1)
            if random.random() < CROSS_OVER_PROBABILITY:
                children = crossover(ind1.gene_list, ind2.gene_list, set_of_rectangles, calculate_fitness,it_rotates)
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
                mutated.append(mutate(ind.gene_list, set_of_rectangles, number_of_rectangles, calculate_fitness,it_rotates))
            else:
                mutated.append(ind)

        population = mutated

        # all values for the best individual in each generation
        best_genes, best_fitness, average_fitness, stack_of_strips, rotation = calculate_best_individual_values(population, set_of_rectangles, it_rotates)

        # best individual's genes
        best_individuals.append(best_genes)

        # best individual's fitness
        best_fitness_acc.append(best_fitness)

        # average fitness
        average_fitness_acc.append(average_fitness)

        # individual's rotation list
        rotations_acc.append(rotation)

        # solution
        solutions.append(stack_of_strips)


    plot_result(average_fitness_acc,MAX_GENERATIONS, RESULTS_FOLDER, "Average fitness")
    plot_result(best_fitness_acc, MAX_GENERATIONS, RESULTS_FOLDER, "Best fitness")

    for j in range(MAX_GENERATIONS):
        print(" -- ")
        print("Generation: ", j)
        print("Best individual: ", best_individuals[j])
        print("Rotation: ", rotations_acc[j])
        print("Solution: ", solutions[j])
        print("Fitness: ", best_fitness_acc[j])

    # Print and save the plots
    #if MAX_GENERATIONS <= 1000:
    # for c in range(MAX_GENERATIONS):
    #    plot_rectangles(set_of_rectangles, solutions[c], best_individuals[c], best_fitness_acc[c], c, W, FOLDER_NFDH)

if __name__ == '__main__':
    data = [(37,11),(26,68),(25,75),(24,17),(20,73),(30,28),(12,35),(25,47),(10,30),(30,50)]
    rectangles = generate_N_ractangles(len(data),data)
    it_rotates = True

    population = create_starting_population(POPULATION_SIZE, rectangles, np.arange(len(data)),calculate_fitness,it_rotates)
    best  = get_best_individual(population)

    chdir("../")
    i =0
    for p in population:

        stack = generate_stack_of_strips(p.gene_list,p.rotation,rectangles,W,it_rotates)
        plot_rectangles(rectangles, stack, p, i, W, "results",it_rotates,"GAr")
        print(p)
        i = i +1