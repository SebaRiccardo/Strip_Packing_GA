
import numpy as np
from math import floor,ceil
from numpy.ma import median
from numpy import mean,std
import os
from rectangle import generate_N_ractangles

#Calculates the maximun height in a strip
def max_height(elements,rectangles,rotation_list,it_rotates):
    heigts = []
    for i in elements:
        height = rectangles[i].height
        # it has to use the width as the height becouse the rectangle "it's rotated by 90 degrees"
        if it_rotates and rotation_list[i] == 1:
            height = rectangles[i].width
        heigts.append(height)
    return max(heigts)

#Generates an array of ones and zeros
def array_of_ones_and_zeros(chromosome_length,seed):

    np.random.seed(seed)
    # number of ones in the list
    number_of_ones = np.random.randint(0,(ceil(chromosome_length/2)+1))
    # array of zeros
    array_zeros = np.zeros(chromosome_length)
    # add ones from 0 to number of ones
    array_zeros[0:number_of_ones] =1
    # shuffle that shit
    np.random.shuffle(array_zeros)

    return list(array_zeros.astype(int))

def strip_width(elements,rectangles,W):
    total =0
    for e in elements:
        total = total+ rectangles[e].width
    return W-total

def generate_stack_of_strips(gene_list, rotation_list, rectangles, max_strip_width,it_rotates):
    list_of_strips =[]
    strip = []
    space_used = 0;

    for i in gene_list:

        if it_rotates and rotation_list[i] == 1:
            # rectangle rotates 90 degrees
            rectangle_width = rectangles[i].height
            rectangle_height = rectangles[i].width
        else:
            rectangle_width = rectangles[i].width
            rectangle_height = rectangles[i].height

        # la regla dice que el ancho de los rectangulos no pueden ser masyor a  W
        if max_strip_width <= (space_used + rectangle_width):

            if len(strip) == 0 and rectangle_width == max_strip_width:
                list_of_strips.append([i])
            else:
                if len(strip) == 0 and rectangle_width < max_strip_width:
                    strip.append(i)
                else:
                    list_of_strips.append(strip.copy())
                    strip = []
                    strip.append(i)

            # because we are in a new strip the space used is equal to the only rectangle's width in it. this being the value of rectangle_width
            space_used = rectangle_width
        else:
            # accumulates the widths of the rectangles of one strip because it's lower than W and there is still space left.
            space_used = space_used + rectangle_width
            strip.append(i)

    list_of_strips.append(strip.copy())

    return list_of_strips

#fitness best and average
def get_best_individual(population):
    return min(population, key = lambda ind: ind.fitness)

def get_average_fitness(population):
    return sum([i.fitness for i in population]) / len(population)

def get_worst_individual(population):
    return max(population, key=lambda ind: ind.fitness)
def stats(population, rectangles, max_width, best_ind, best_fitness, average_fitness, best_fitness_ever, it_rotates):

    # Best individual for the current generation
    best_of_generation = get_best_individual(population)

    # checks if the current best is better that the best ever
    if best_ind.fitness > best_of_generation.fitness:
       best_ind = best_of_generation

    best_fitness.append(best_of_generation.fitness)
    average_fitness.append(get_average_fitness(population))
    best_fitness_ever.append(min(best_fitness+best_fitness_ever))
    #stack_of_strips = generate_stack_of_strips(best_of_generation.gene_list,best_of_generation.rotation, rectangles, max_width, it_rotates)


    return best_ind, best_of_generation, best_fitness, average_fitness, best_fitness_ever

def get_values_from_files(file_name):
    # navigate to the folder where the txt files are located
    os.chdir("../")
    os.chdir("./instances")
    dir = os.getcwd()
    file = open(dir + "\\" + file_name, "r")
    os.chdir("../")
    os.chdir("./src")

    lines = file.readlines()
    file.close()
    trimmed_lines= np.char.strip(lines, chars="\n")

    # in de index 0 we have the W of the instance
    max_width = int(trimmed_lines[0])
    values =trimmed_lines[1:]
    rectangles_values = []
    #values = ['4 15','15 3' ... ,'10 3']
    for value in values:
       dimensions=np.array(value.split()) # value= "2 10" that correspond to the width and the height of one rectangle.
       dimensions= dimensions.astype(int) # so we split it and assign it to an array called dimensions = [2,10] and convert each element to integer
       rectangles_values.append(tuple(dimensions))

    return len(rectangles_values) , rectangles_values , max_width

def calculate_stats_per_instance(individuals,number_of_rectangles, rectangles_values, max_width, it_rotates):

    best_ind = get_best_individual(individuals)
    worst_ind = get_worst_individual(individuals)
    rectangles =generate_N_ractangles(number_of_rectangles,rectangles_values)
    stack = generate_stack_of_strips(best_ind.gene_list, best_ind.rotation, rectangles, max_width,it_rotates)

    solution = best_ind

    best_fitness = best_ind.fitness
    worst_fitness = worst_ind.fitness
    fitness_list = [i.fitness for i in individuals]
    fitness_list.sort(key=lambda fitness:fitness)

    fit_mean = mean(fitness_list)
    fit_median = median(fitness_list)
    stard_deviation = std(fitness_list)

    return fit_median, fit_mean, best_fitness,worst_fitness, stard_deviation, solution, stack


def save_to_file(statics,algorithm_type,folder):

    os.chdir("../")
    os.chdir("./results")
    dir = os.getcwd()
    for key,value in statics.items():
        f = open(folder+"/Results_"+algorithm_type+"_"+key+".txt" , "w")
        f.write("--------------------RESULTS "+ str(algorithm_type)+" - "+key+"-----------------------\n\r")
        for key,value in value.items():

            f.write("- "+str(key) +": "+str(value)+"\n\r")
        f.write("---------------------------------------------------------------------------------")
        f.close()
    return 1

def print_stats(statics,algorithm_type):

    for key, value in statics.items():
        print("--------------------------------------"+key+"--------------------------------------")
        print("--------------" + str(algorithm_type) + " - " + key + "--------------\n\r")
        for key, value in value.items():
            print("- " + str(key) + ": " + str(value) + "\n\r")
        print("--------------------------------------<END>---------------------------------------")
    return 1