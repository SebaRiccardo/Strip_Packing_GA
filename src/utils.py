
import numpy as np
from GLOBAL import  W
from math import floor,ceil

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

    #np.random.seed(seed)
    #number of ones in the list
    number_of_ones = np.random.randint(0,(ceil(chromosome_length/2)+1))
    #array of zeros
    array_zeros = np.zeros(chromosome_length)
    #add ones from 0 to number of ones
    array_zeros[0:number_of_ones] =1
    #shuffle that shit
    np.random.shuffle(array_zeros)

    return array_zeros

#fitness best and average
def get_best_individual(population):
    return min(population, key = lambda ind: ind.fitness)

def get_average_fitness(population):
    return sum([i.fitness for i in population]) / len(population)

def strip_width(elements,rectangles,W):
    total =0
    for e in elements:
        total = total+ rectangles[e].width
    return W-total

def generate_stack_of_strips(gene_list, rotation_list, rectangles, max_strip_width,it_rotates):
    list_of_strips =[]
    strip = []
    sum_of_widths = 0;

    for i in gene_list:

        rectangle_width = 0
        rectangle_height = 0

        if it_rotates and rotation_list[i] == 1:
            # rectangle rotates 90 degrees
            rectangle_width = rectangles[i].height
            rectangle_height = rectangles[i].width
        else:
            rectangle_width = rectangles[i].width
            rectangle_height = rectangles[i].height

        # la regla dice que el ancho de los rectangulos no pueden ser masyor a  W
        if max_strip_width <= (sum_of_widths + rectangle_width):
            aux = strip
            # ya complete un strip porque si agrego el proximo supera el W =100
            list_of_strips.append(aux)
            strip =[]
            # sumo el ancho del nuevo rectangulo en el strip nuevo
            sum_of_widths = rectangle_width
        else:
            sum_of_widths = sum_of_widths + rectangle_width

        strip.append(i)

    # Lista de strips donde en cada strip estan los triangulos.
    list_of_strips.append(strip)

    return list_of_strips

def calculate_best_individual_values(population, rectangles, it_rotates):

    # Best individual for the current generation
    best_one = get_best_individual(population)
    best_fitness = best_one.fitness
    average_fitness = get_average_fitness(population)
    stack_of_strips = generate_stack_of_strips(best_one.get_gene_list(),best_one.get_rotation(), rectangles, W, it_rotates)
    best_genes = best_one.get_gene_list()
    rotation = best_one.get_rotation()

    return best_genes,best_fitness,average_fitness,stack_of_strips, rotation
