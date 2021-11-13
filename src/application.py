import os
import random
import numpy as np
from os import chdir
from rectangle import generate_N_ractangles
from selection import select_tournament
from crossover import crossover
from mutate import mutate
from population import create_starting_population
from fitness import calculate_fitness
from utils import generate_stack_of_strips, get_best_individual, get_average_fitness, stats,get_values_from_files
from plotting import plot_result, plot_rectangles,generate_animation,add_text_below,plot_individual_info,print_individual,print_best_individual
from GLOBAL import POPULATION_SIZE, MAX_GENERATIONS, MUTATION_PROBABILITY, CROSS_OVER_PROBABILITY,TOURNAMENT_SIZE,RESULTS_FOLDER

def GA(number_of_rectangles, values, W, genes, it_rotates,seed):
    solutions = []
    best_individuals = []
    best_fitness_acc = []
    average_fitness_acc = []
    rotations_acc =[]

    random.seed(seed)

    # Generate reference rectangle list
    set_of_rectangles = generate_N_ractangles(number_of_rectangles,values)

    # Start inicial population
    population = create_starting_population(POPULATION_SIZE, W, set_of_rectangles, genes, calculate_fitness, it_rotates,seed)

    # gets the initial best individual and average fitness
    best_ind = get_best_individual(population)
    average_fitness = get_average_fitness(population)
    best_fitness = best_ind.fitness
    best_fitness_ever =
    best_ind = random.choice(population)

    # prints the best individual
    #print_best_individual(best_one, average_fitness, set_of_rectangles, W, it_rotates)
    # Plot the info of the first individual
    #plot_individual_info(best_one,W, set_of_rectangles,RESULTS_FOLDER, it_rotates)

    for generation_number in range(MAX_GENERATIONS):
        # SELECTION
        selected = select_tournament(population, TOURNAMENT_SIZE)
        # CROSSOVER
        crossed_offspring = []
        for ind1, ind2 in zip(selected[::2], selected[1::2]):
            if random.random() < CROSS_OVER_PROBABILITY:
                children = crossover(ind1.gene_list, ind2.gene_list, max_width, set_of_rectangles, calculate_fitness,it_rotates)
                crossed_offspring.append(children[0])
                crossed_offspring.append(children[1])
            else:
                crossed_offspring.append(ind1)
                crossed_offspring.append(ind2)
        # MUTATION
        mutated = []
        for ind in crossed_offspring:
            if random.random() < MUTATION_PROBABILITY:
                mutated.append(mutate(ind.gene_list, max_width, set_of_rectangles, number_of_rectangles, calculate_fitness,it_rotates))
            else:
                mutated.append(ind)
        population = mutated.copy()

        # all values for the best individual in each generation
        best_genes, best_fitness, average_fitness_acc, stack_of_strips, rotation = stats(population, set_of_rectangles,W, best_ind, average_fitness_acc , t_rotates)

        # best individual's genes
        best_individuals.append(best_genes)

        # best individual's fitness
        best_fitness_acc.append(best_fitness)


        # individual's rotation list
        rotations_acc.append(rotation)

        # solution
        solutions.append(stack_of_strips)

    return
    #for j in range(MAX_GENERATIONS):
    #    print_individual(j, best_individuals[j], rotations_acc[j], solutions[j], best_fitness_acc[j])

def test():
    data = [(50, 25), (50, 25), (30, 60), (30, 60)]
    rectangles = generate_N_ractangles(len(data), data)
    it_rotates = True

    population = create_starting_population(POPULATION_SIZE, rectangles, np.arange(len(data)), calculate_fitness,
                                            it_rotates)
    best = get_best_individual(population)

    chdir("../")
    i = 0
    images =[]
    for p in population:
        stack = generate_stack_of_strips(p.gene_list, p.rotation, rectangles, W, it_rotates)
        fig= add_text_below(p,rectangles,it_rotates,-0.07,.02,3,3,"black")
        plot_rectangles(fig,rectangles, stack, p, i, W, "results", it_rotates, "GAr")
        print(p)
        i = i + 1

def test2(rectangles):
    result =calculate_fitness([0, 3, 5, 1, 2, 7, 4, 6, 8],[1, 1, 1, 0, 1, 0, 0, 0, 1],rectangles,15,True)


def experimental(iterations):

    instances = {
        "I1": "spp9a.txt",
        "I2": "spp9b.txt",
        "I3": "spp10.txt",
        "I4": "spp11.txt",
        "I5": "spp12.txt",
        "I6": "spp13.txt",
    }

    W = max_width
    genes = np.arange(number_of_rectangles)  # e.g: [0,1,2,3,4,5,6 ... (number_of_rectangles-1)]

    for key,value in instances.values():

        number_of_rectangles, rectangles_values, max_width = get_values_from_files(value)

        rotation = True
        seeds = np.arange(20) # seeds
        for mode in range(2): # mode rotation and mode no-rotation

            for i in range(iterations): #20 iterations

                GA(number_of_rectangles,rectangles_values,max_width,genes,rotation,seeds[i])


if __name__ == '__main__':

    options = {
        "rotation": 1,
        "experimental":0
    }

    print("1. STRIP PACKING GA WITH ROTATION ")
    print("2. STRIP PACKING GA WITHOUT ROTATION")
    value= input("->:")
    options["rotation"]  = int(value)

    while options["rotation"]!= 1 and options["rotation"]!= 2:
        print("Choose a valid option,please:")
        print("1. STRIP PACKING GA WITH ROTATION ")
        print("2. STRIP PACKING GA WITHOUT ROTATION")
        options["rotation"] = int(input(""))

    """     
    if options["rotation"] == 1:
        # with rotation
        #test2(generate_N_ractangles(number_of_rectangles,rectangles_values))
        GA(number_of_rectangles, rectangles_values, W ,genes, True,0)
    else:
        # without rotation
        GA(number_of_rectangles, rectangles_values, W ,genes, False,0)
    """