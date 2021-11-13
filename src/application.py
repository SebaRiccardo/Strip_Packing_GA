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
from utils import generate_stack_of_strips, get_best_individual, get_average_fitness, calculate_best_individual_values,get_values_from_files
from plotting import plot_result, plot_rectangles,generate_animation,add_text_below,plot_individual_info
from GLOBAL import POPULATION_SIZE, MAX_GENERATIONS, MUTATION_PROBABILITY, CROSS_OVER_PROBABILITY,TOURNAMENT_SIZE,RESULTS_FOLDER

def GA(number_of_rectangles, values, W, genes, it_rotates):
    solutions = []
    best_individuals = []
    best_fitness_acc = []
    average_fitness_acc = []
    rotations_acc =[]

    # Generate reference rectangle list
    set_of_rectangles = generate_N_ractangles(number_of_rectangles,values)

    # Start inicial population
    population = create_starting_population(POPULATION_SIZE, W, set_of_rectangles, genes,calculate_fitness,it_rotates)

    # Calculates the best and average for que starting population
    initial_best_genes, initial_best_fitness, initial_average_fitness, initial_stack_of_strips, initial_rotation = calculate_best_individual_values(population,set_of_rectangles,it_rotates)

    # Print the info of the first individual
    plot_individual_info(W, set_of_rectangles, initial_best_genes, initial_best_fitness, initial_rotation,
                             initial_average_fitness, initial_stack_of_strips, RESULTS_FOLDER, it_rotates)

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
        best_genes, best_fitness, average_fitness, stack_of_strips, rotation = calculate_best_individual_values(population, W, set_of_rectangles, it_rotates)

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

    #plot_result(average_fitness_acc,MAX_GENERATIONS, RESULTS_FOLDER, "Average fitness")
    #plot_result(best_fitness_acc, MAX_GENERATIONS, RESULTS_FOLDER, "Best fitness")

    for j in range(MAX_GENERATIONS):
        print(" -- ")
        print("Generation: ", j)
        print("Best individual: ", best_individuals[j])
        print("Rotation: ", rotations_acc[j])
        print("Solution: ", solutions[j])
        print("Fitness: ", best_fitness_acc[j])

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

if __name__ == '__main__':
    instances ={
        "I1": "spp9a.txt",
        "I2": "spp9b.txt",
        "I3": "spp10.txt",
        "I4": "spp11.txt",
        "I5": "spp12.txt",
        "I6": "spp13.txt",
    }
    options = {
        "rotation": 0
    }
    print("1. STRIP PACKING GA WITH ROTATION ")
    print("2. STRIP PACKING GA WITHOUT ROTATION")
    value= input("->:")
    options["rotation"]  = int(value)

    while options["rotation"]!= 1 and options["rotation"]!= 2:
        print("Choose a valid option,please:")
        print("1. STRIP PACKING GA WITH ROTATION ")
        print("2. STRIP PACKING GA WITHOUT ROTATION")
        options["rotation"] =int(input(""))

    # navigate to the folder where the txt files are located
    os.chdir("../")
    os.chdir("./instances")
    dir = os.getcwd()
    file = open(dir + "\\" + instances["I1"], "r")


    number_of_rectangles,rectangles_values,max_width = get_values_from_files(file)

    W = max_width
    genes = np.arange(number_of_rectangles) #e.g: [0,1,2,3,4,5,6 ... (number_of_rectangles-1)]

    if options["rotation"] == 1:
        # with rotation
        GA(number_of_rectangles, rectangles_values, W ,genes, True)
    else:
        # without rotation
        GA(number_of_rectangles, rectangles_values, W ,genes, False)
