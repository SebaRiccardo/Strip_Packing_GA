import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
from utils import max_height,generate_stack_of_strips,get_average_fitness,get_values_from_files,sort_by_height
from rectangle import generate_N_ractangles
from GLOBAL import RECTANGLES_NUMBER,instances
import matplotlib._color_data as mcd

def plot_result(best_fitness,generation_number,type):
    generations_list =np.arange(1,generation_number+1)
    plt.plot(best_fitness)

    plt.xlabel('Generation')
    plt.ylabel(type)
    # save the figure
    dir = os.getcwd()
    plt.savefig(dir+"\%s.png" % (folder,type), dpi=100, bbox_inches='tight')
    plt.show()
    plt.close()
# all fun that are used to plot the results

def add_text_below(individual,rectangles,it_rotates,initY,initX,items_count,colums_count,default_color):
    fig = plt.figure()
    x_off_set = .25
    y = initY
    x = initX
    items = 0
    row_height = 0
    colums = 0
    color = default_color
    for rec in rectangles:
        # if rectangle rotates it's printed in red color
        if it_rotates and individual.rotation[rec.number] == 1:
            color = "red"
        else:
            color = "black"

        fig.text(x, y, rec, color=color)
        items += 1
        y = y - .04

        if items == items_count:
            # new item added
            items = 0
            colums += 1
            row_height = y
            y = initY
            x = x + x_off_set

        if colums == colums_count:
            # start adding new items below the first row of items
            colums = 0
            x = initX
            y = row_height - .025
            initY = y
    return fig

def generate_plots(fig, rectangles, stack, individual, max_strip_width, it_rotates, subtitle):
    #fig = plt.figure()
    ax = fig.add_subplot()
    fig.suptitle(subtitle)
    prevIndex = -1
    colors = [name for name in mcd.CSS4_COLORS
               if "xkcd:" + name in mcd.XKCD_COLORS]
    colors.remove("white")
    Xaxis = 0
    Yaxis = 0
    #individual: [1,3,4,5,3,2]
    # stack: [[1,3,4],[5,3,2]]
    for strip in stack:
        Xaxis = 0
        # strip: [1,3,4]
        for i in strip:
            rectangle_width = 0
            rectangle_height = 0

            if it_rotates and individual.rotation[i] == 1:
                # rectangle rotates 90 degrees
                rectangle_width = rectangles[i].height
                rectangle_height = rectangles[i].width
            else:
                rectangle_width = rectangles[i].width
                rectangle_height = rectangles[i].height

            # if the amount the colors is grater than rectangles we can safely use fixed colors for each rectangle otherwise we MUST use random colors
            # thus repeated colors
            if len(colors) >= RECTANGLES_NUMBER:
                indexColor = i
            else:
                indexColor= np.random.randint(0,len(colors))
                while indexColor == prevIndex:
                      indexColor = np.random.randint(0, len(colors))

            prevIndex = indexColor
            rectangle = matplotlib.patches.Rectangle((Xaxis,Yaxis),rectangle_width,rectangle_height,edgecolor='black',facecolor=colors[indexColor],linewidth=0.3,alpha =0.6)

            #X axis the acc of widths
            Xaxis = Xaxis+ rectangle_width
            #add the rectangle to the ax
            ax.add_patch(rectangle)
            rx, ry = rectangle.get_xy()
            cx = rx + rectangle.get_width() / 2.0
            cy = ry + rectangle.get_height() / 2.0
            ax.annotate(str("R"+str(i)), (cx, cy), color='black', weight='normal', fontsize=10, ha='center', va='center')

        Yaxis +=  max_height(strip,rectangles,individual.rotation,it_rotates)
        ax.axhline(y=Yaxis,linewidth=.5,color='#d62728')

    plt.ylabel("Height")
    plt.xlabel("Width")
    fig.text(0.02, -0.0, "MAX WIDTH:" + str(max_strip_width))
    fig.text(0.02, -0.05, "Fitness:" + str(individual.fitness))
    fig.text(0.02, -0.10, "Chromosome:" + str(individual.gene_list))
    fig.text(0.02, -0.15, "Solution:" + str(stack))
    if it_rotates: fig.text(0.02, -0.20, "Rotation: " + str(individual.rotation))
   # plt.axis([0,max_strip_width,0,Yaxis])
    plt.xlim([0, max_strip_width])
    plt.ylim([0, Yaxis])

    return plt

def show_plot(plt):
    plt.show()

def save_plot(plt,filename):

    dir = os.getcwd()
    # save the figure
    plt.savefig(dir+"\%s.png" % (filename), dpi=200, bbox_inches='tight')

def plot_all_instance_solutions(statistics,folders):
    # statistics = [GAr_statistics , GAnr_statistics]
    rotate = [True , False]
    title = ["Genetic Algorithm with rotation","Genetic Algorithm with NO rotation"]
    title_index = 0
    for stats in statistics: # iterates over the first statistics of GA with rotation and then without rotation
        for key, value in stats.items():
            number_of_rectangles, rectangles_values, max_width = get_values_from_files(str(instances[key]))
            rectangles = generate_N_ractangles(number_of_rectangles,rectangles_values)
            #plot rectangles assumes that you are in the folder /Strip_Packing_GA
            # so we have to go up from src to results
            os.chdir("../") # goes up to strip_packing_GA and the goes down to results/GAr
            os.chdir("./results/"+folders[title_index])
            ind = value["Individual"]
            stack = value["Solution"]
            # Instance 1 GAr/ GAnr
            subtitle = title[title_index]+" "+str(key)
            fig = add_text_below(ind, rectangles, rotate[title_index], -0.3, .02, 4, 4, "black")
            plt = generate_plots(fig, rectangles, stack, ind, max_width, rotate[title_index], subtitle)

            save_plot(plt,subtitle)
            os.chdir("../") # goes up from /results/GAr to /results
        title_index =+1 #this is used to iterate over title = ["Genetic Algorithm with rotation","Genetic Algorithm with NO rotation"]
    os.chdir("../")


def plot_individual_info(individual,W,rectangles,RESULTS_FOLDER,it_rotates,file_name):

    initial_stack_of_strips = generate_stack_of_strips(individual.gene_list,individual.rotation,rectangles,W,it_rotates)


    if it_rotates:
        subtitle = "GAr  - "+file_name
    else:
        subtitle = "GAnr - "+file_name

    fig = add_text_below(individual, rectangles, it_rotates, -0.3, .02, 4, 4, "black")
    plt = generate_plots(fig, rectangles, initial_stack_of_strips, individual, W,it_rotates, subtitle)
    save_plot(plt,file_name)
    show_plot(plt)
    plt.close()

def print_best_individual(individual,average_fitness,rectangles,W,it_rotates):

    stack_of_strips = generate_stack_of_strips(individual.gene_list, individual.rotation, rectangles, W,it_rotates)

    print("-----------------------------------------------------")
    print("Best Initial individual: ", individual.gene_list)
    print("Best Initial Fitness: ", individual.fitness)
    print("Rotation: ", individual.rotation)
    print("Initial population Average fitness: ", average_fitness)
    print("Solution: ", stack_of_strips)
    print("-----------------------------------------------------")

def print_individual(best_individual,rotation,fitness):

    print("|  Chromosome: ", best_individual)
    print("|  Rotation: ", rotation)
    print("|  Fitness: ", fitness)

def plot_stats(fit_avg, fit_best, fit_best_ever, it_rotates,TSIZE):

    if it_rotates:
        title = "GA with rotation"
    else:
        title = "GA with NO rotation"

    plt.plot(fit_avg, label = "Average Fitness of Generation")
    plt.plot(fit_best, label = "Best Fitness of Generation")
    plt.plot(fit_best_ever, label = "Best Fitness Ever")
    plt.title(title)
    plt.suptitle("Tournament size: "+ str(TSIZE))
    plt.xlabel("Generations")
    plt.ylabel("Height")
    plt.legend(loc = "upper right")
    dir = os.getcwd()
    plt.savefig(dir + "\stats_%s.png" % (title), dpi=200, bbox_inches='tight')
    plt.show()
    plt.close()