import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
from utils import max_height
from GLOBAL import RECTANGLES_NUMBER
import matplotlib._color_data as mcd

def plot_result(best_fitness,generation_number,folder,type):
    generations_list =np.arange(1,generation_number+1)
    plt.plot(best_fitness)

    plt.xlabel('Generation')
    plt.ylabel(type)
    # save the figure
    dir = os.getcwd()
    plt.savefig(dir+"\%s\%s.png" % (folder,type), dpi=100, bbox_inches='tight')
    plt.show()

def add_text_below(individual,rectangles,it_rotates,initY,initX,items_count,colums_count,default_color):
    fig = plt.figure()
    x_off_set = .18
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
            y = row_height - .02
            initY = y
    return fig

def plot_rectangles(fig,rectangles,stack,individual,generation_number,max_strip_width,folder,it_rotates,subtitle):

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
    fig.text(0.02,-0.02,"Generation: " + str(generation_number) + " " + str(individual))
   # plt.axis([0,max_strip_width,0,Yaxis])
    plt.xlim([0, max_strip_width])
    plt.ylim([0, Yaxis])

    dir = os.getcwd()

    # save the figure
    plt.savefig(dir+"\%s\generation_%a.png" % (folder,generation_number), dpi=200, bbox_inches='tight')
    #plt.show()
    plt.close(fig)

def plot_individual_info(W,set_of_rectangles,initial_best_genes,initial_best_fitness,initial_rotation,initial_average_fitness,initial_stack_of_strips,RESULTS_FOLDER,it_rotates):
    print("-------RECTANGLES----------")
    for rec in set_of_rectangles:
        print(rec)
    print("-----------------------------------------------------")
    print("Best Initial individual: ", initial_best_genes)
    print("Best Initial Fitness: ", initial_best_fitness)
    print("Rotation: ", initial_rotation)
    print("Initial population Average fitness: ", initial_average_fitness)
    print("Solution: ", initial_stack_of_strips)
    print("-----------------------------------------------------")
    plot_rectangles(set_of_rectangles, initial_stack_of_strips, initial_best_genes, initial_best_fitness, "initial", W,RESULTS_FOLDER, it_rotates)

def generate_animation(images):
    frames = []


    for image in images:
        im = image.imshow()
        frames.append([im])
    ani = animation.ArtistAnimation(fig,frames)
    ani.save("generations.mp4")