import os
import random
import numpy as np
from os import chdir
import time
from rectangle import generate_N_ractangles,generate_rectangles
from selection import select_tournament
from crossover import crossover
from mutate import mutate
from population import create_starting_population
from fitness import calculate_fitness
from utils import generate_stack_of_strips,get_best_individual, get_average_fitness, \
    stats,get_values_from_files,calculate_stats_per_instance,save_to_file,print_stats,stats_experimental
from plotting import plot_result, generate_plots,add_text_below,plot_individual_info,print_individual,print_best_individual,plot_stats,plot_all_instance_solutions
from GLOBAL import POPULATION_SIZE, MAX_GENERATIONS, MUTATION_PROBABILITY, CROSS_OVER_PROBABILITY,TOURNAMENT_SIZE,RESULTS_FOLDER,instances,RECTANGLES_NUMBER,MAX_WIDTH

##-----------------------------------GA main flow-----------------------------##
def GA(number_of_rectangles, values, W, genes, it_rotates,seed,run_number):

    random.seed(seed)
    # Generate reference rectangle list
    set_of_rectangles = generate_N_ractangles(number_of_rectangles,values)
    # Start inicial population
    population = create_starting_population(POPULATION_SIZE, W, set_of_rectangles, genes, calculate_fitness, it_rotates,seed)

    # initial stats
    best_ind = get_best_individual(population)
    #average_fitness = [get_average_fitness(population)]
    best_fitness = [best_ind.fitness]
    best_individuals = [best_ind]
    best_fitness_ever = [best_ind.fitness]

    for generation_number in range(MAX_GENERATIONS):
        new_seed = (seed+generation_number)
        # SELECTION
        selected = select_tournament(population, TOURNAMENT_SIZE, new_seed)
        # CROSSOVER
        crossed_offspring = []
        for ind1, ind2 in zip(selected[::2], selected[1::2]):
            if random.random() < CROSS_OVER_PROBABILITY:
                children = crossover(ind1, ind2, W, set_of_rectangles, calculate_fitness, new_seed, it_rotates)
                crossed_offspring.append(children[0])
                crossed_offspring.append(children[1])
            else:
                crossed_offspring.append(ind1)
                crossed_offspring.append(ind2)
        # MUTATION
        mutated = []
        for ind in crossed_offspring:
            if random.random() < MUTATION_PROBABILITY:
                mutated.append(mutate(ind.gene_list, ind.rotation, W, set_of_rectangles, number_of_rectangles, calculate_fitness, new_seed, it_rotates))
            else:
                mutated.append(ind)
        population = mutated.copy()

        # all values for the best individual in each generation
        best_ind, best_of_generation, best_fitness, best_fitness_ever = \
            stats_experimental(population, set_of_rectangles, W, best_ind, best_fitness,best_fitness_ever)

    return best_ind
#-----------------------------------------------------------------------------##

def default_GA(number_of_rectangles, W, genes, it_rotates,seed,GENERATIONS,TOURNAMENT_SIZE):

    random.seed(seed)

    # Generate reference rectangle list
    set_of_rectangles = generate_rectangles(number_of_rectangles,seed)

    # Start inicial population
    population = create_starting_population(POPULATION_SIZE, W, set_of_rectangles, genes, calculate_fitness, it_rotates,seed)

    # print("-----------------First population-------------------")
    #for p in population:
    #     print(p)
    # print("----------------------<****>--------------------------")

    # initial stats
    best_ind = get_best_individual(population)
    average_fitness = [get_average_fitness(population)]
    best_fitness = [best_ind.fitness]
    best_individuals = [best_ind]
    best_fitness_ever = [best_ind.fitness]

    #prints the best individual
    print_best_individual(best_ind, average_fitness[0], set_of_rectangles, W, it_rotates)

    # Plot the info of the first individual
    plot_individual_info(best_ind, W, set_of_rectangles, RESULTS_FOLDER, it_rotates,"First Individual")

    for generation_number in range(GENERATIONS):
        # SELECTION
        selected = select_tournament(population, TOURNAMENT_SIZE, seed+generation_number)
        # CROSSOVER
        crossed_offspring = []
        for ind1, ind2 in zip(selected[::2], selected[1::2]):
            if random.random() < CROSS_OVER_PROBABILITY:
                children = crossover(ind1, ind2, W, set_of_rectangles, calculate_fitness, seed+generation_number, it_rotates)
                crossed_offspring.append(children[0])
                crossed_offspring.append(children[1])
            else:
                crossed_offspring.append(ind1)
                crossed_offspring.append(ind2)
        # MUTATION
        mutated = []
        for ind in crossed_offspring:
            if random.random() < MUTATION_PROBABILITY:
                mutated.append(mutate(ind.gene_list, ind.rotation, W, set_of_rectangles, number_of_rectangles, calculate_fitness, seed+generation_number, it_rotates))
            else:
                mutated.append(ind)
        population = mutated.copy()

        # all values for the best individual in each generation
        best_ind, best_of_generation, best_fitness, average_fitness, best_fitness_ever = \
            stats(population, set_of_rectangles, W, best_ind, best_fitness, average_fitness, best_fitness_ever)
        #print("Best of generation: %i "%(generation_number+1),best_of_generation)
    print("|----------------------------------------|")
    print("|  Best individual generated by the GA   |")
    print_individual(best_ind.gene_list,best_ind.rotation,best_ind.fitness)
    print("|----------------------------------------|")
    plot_stats(average_fitness, best_fitness, best_fitness_ever,it_rotates,TOURNAMENT_SIZE)
    plot_individual_info(best_ind, W, set_of_rectangles, RESULTS_FOLDER, it_rotates, "Best Individual")
    return best_ind
##-----------------------------------<->--------------------------------------##

#------ execution mode main flow--------#
def experimental(number_of_runs,seed):
    np.random.seed(seed)
    GAr_statistics = {}
    GAnr_statistics = {}

    # iterates over the whole instances
    for key,value in instances.items():

        #best individual in the 20 runs
        number_of_rectangles, rectangles_values, max_width = get_values_from_files(value)

        print("------- Running instance %s ----------" % (value))
        print("------- RECTANGLES ----------")
        print(rectangles_values)

        genes = np.arange(number_of_rectangles) # e.g: [0,1,2,3,4,5,6 ... (number_of_rectangles-1)]
        seeds = np.arange(number_of_runs) # seeds
        np.random.shuffle(seeds)
        modes = [True,False]  # with rotation and without rotation

        #runs the GA in  mode rotation and mode no-rotation x number_of_runs
        for mode in modes:
            best_individuals = []
            #print("Starting " +str(number_of_runs)+ " runs in with rotation enable: " + str(mode))
            start = time.time()
            for run in range(number_of_runs): #20 runs
               best_individuals.append(GA(number_of_rectangles,rectangles_values,max_width,genes,mode,seeds[run],run))
            end = time.time()

            if mode:
                execution_time_GAr = (end - start)
                best_individual_GAr = best_individuals.copy()
            else:
                execution_time_GAnr = (end - start)
                best_individual_GAnr = best_individuals.copy()

        #calculate all the stats for the two modes
        GAr_median, GAr_mean, GAr_best_fitness,GAr_worst_fitness, GAr_stard_deviation, GAr_solution,GAr_stack = \
            calculate_stats_per_instance(best_individual_GAr,number_of_rectangles, rectangles_values, max_width, True)

        GAnr_median, GAnr_mean, GAnr_best_fitness,GAnr_worst_fitness, GAnr_stard_deviation, GAnr_solution,GAnr_stack = \
            calculate_stats_per_instance(best_individual_GAnr,number_of_rectangles, rectangles_values, max_width, False)

        #save results per instance in a dic
        GAr_statistics[key] = {
                               "Runs": number_of_runs,
                               "Generations per run": MAX_GENERATIONS,
                               "Population size":  POPULATION_SIZE,
                               "Rectangles number": number_of_rectangles,
                               "Crossover probability": CROSS_OVER_PROBABILITY,
                               "Mutation probability": MUTATION_PROBABILITY,
                               "Tournament size": TOURNAMENT_SIZE,
                               "Median": GAr_median,
                               "Mean": GAr_mean,
                               "Best fitness": GAr_best_fitness,
                               "Worst fitness":GAr_worst_fitness,
                               "Standard deviation": GAr_stard_deviation,
                               "Individual" :GAr_solution,
                               "Solution": GAr_stack,
                               "Execution time (seg)": execution_time_GAr
                               }

        GAnr_statistics[key] = {
                               "Runs": number_of_runs,
                               "Generations per run": MAX_GENERATIONS,
                               "Population size": POPULATION_SIZE,
                               "Rectangles number": number_of_rectangles,
                               "Crossover probability": CROSS_OVER_PROBABILITY,
                               "Mutation probability": MUTATION_PROBABILITY,
                               "Tournament size": TOURNAMENT_SIZE,
                               "Median": GAnr_median,
                               "Mean": GAnr_mean,
                               "Best fitness": GAnr_best_fitness,
                               "Worst fitness": GAnr_worst_fitness,
                               "Standard deviation": GAnr_stard_deviation,
                               "Individual" :GAnr_solution,
                               "Solution": GAnr_stack,
                               "Execution time (seg)": execution_time_GAnr
                               }

    return GAr_statistics , GAnr_statistics


#------ default mode main flow -------- #
def default_mode(values_mode,it_rotates):
    #seed = random.randint(1, 100)
    seed = 1
    genes = np.arange(RECTANGLES_NUMBER)
    if values_mode == 1:
        best_ind = default_GA(RECTANGLES_NUMBER, MAX_WIDTH, genes, it_rotates, seed, MAX_GENERATIONS, TOURNAMENT_SIZE)
    else:
        max_generations = option_selector("insert Max number of generations( n >0)")
        tournament_size = option_selector("insert tournament size ( n > 0)")
        best_ind = default_GA(RECTANGLES_NUMBER, MAX_WIDTH, genes, it_rotates, seed, max_generations, tournament_size)
    return  best_ind



#---------------- menues ----------------#
def default_mode_menu(options):
    print("Choose a valid option,please:")
    print("1. Strip Packing GA with rotation")
    print("2. Strip Packing GA without rotation")
    value = input("->")
    options["rotation"] = int(value)

    while options["rotation"] != 1 and options["rotation"] != 2:
        print("Choose a valid option,please:")
        print("1. Strip Packing GA with rotation")
        print("2. Strip Packing GA without rotation")
        options["rotation"] = int(input("->"))

    valid_options = ["1. Use default values", "2. Use custom values"]
    options["values_mode"] = multi_option_selector(valid_options)

    return options

def option_selector(opt1):
    print(opt1)
    value = input("->")
    options = int(value)

    while options <= 0:
        print("Insert a valid value:")
        print(opt1)
        value = input("->")
        options = int(value)
    return options

def multi_option_selector(options):

    for opt in options:
        print(opt)

    value = int(input(""))

    while value < 1 or value > len(options):
        print("Insert a valid option:")

        for opt in options:
            print(opt)
        value = int(input(""))
    return value


########################### ---- MAIN ---- ################################
if __name__ == '__main__':

    options = {
        "rotation": 0,
        "experimental":0,
        "values_mode":-1
    }

    print("1. Experimental mode")
    print("2. Default mode")
    value = input("")
    options["experimental"] = int(value)

    while options["experimental"]!= 1 and options["experimental"]!= 2:
        print("Choose a valid option,please:")
        print("1. Experimental mode")
        print("2. Default mode")
        options["experimental"] = int(input(""))

    if options["experimental"] == 1:
        runs = 20
        folders = ["GAr","GAnr"]
        input_seed=option_selector("Insert a seed number: (s>=0)")
        #experimental mode
        start  = time.time()
        GAr_statistics, GAnr_statistics = experimental(runs,input_seed)
        end = time.time()
        EXECUTION_TIME = (end - start)
        if EXECUTION_TIME >= 60:
            print("****************************************************************")
            print("EXECUTION TIME (min):", EXECUTION_TIME/60 )
            print("****************************************************************")
        else:
            print("****************************************************************")
            print("EXECUTION TIME (seg):", EXECUTION_TIME )
            print("****************************************************************")

        opt = multi_option_selector(["1. Print results in console","2. Save results in .txt files","3. Generate plots","4. All"])
        #menu for printing or ploting
        if opt == 1:
            print_stats(GAr_statistics, "Genetic Algorithm with rotation")
            print_stats(GAnr_statistics, "Genetic Algorithm with NO rotation")
        elif opt == 2:
            print("Saving results to files...")
            save_to_file(GAr_statistics, "Genetic Algorithm with rotation", folders[0])
            save_to_file(GAnr_statistics, "Genetic Algorithm with NO rotation", folders[1])
            print("Results saved! in folder /results")
        elif opt == 3:
            print("Generating plots..")
            statistics = [GAr_statistics, GAnr_statistics]
            # print results
            plot_all_instance_solutions(statistics, folders)
            print("Plots generated! and saved in /results folder")
        elif opt == 4:
            print("****************************************************************")
            print_stats(GAr_statistics, "Genetic Algorithm with rotation")
            print_stats(GAnr_statistics, "Genetic Algorithm with NO rotation")
            print("****************************************************************")
            print("Saving to files...")
            save_to_file(GAr_statistics, "Genetic Algorithm with rotation", folders[0])
            save_to_file(GAnr_statistics, "Genetic Algorithm with NO rotation", folders[1])
            os.chdir("../")
            os.chdir("./src")
            print("Results saved! in folder /results")
            print("****************************************************************")
            print("Generating plots..")
            statistics = [GAr_statistics, GAnr_statistics]
            plot_all_instance_solutions(statistics, folders)
            print("Plots generated! and saved in /results folder")
    else:
        options = default_mode_menu(options)
        if options["rotation"]==1:
            default_mode(options["values_mode"],True)
        else:
            default_mode(options["values_mode"],False)
