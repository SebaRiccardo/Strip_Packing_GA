import numpy as np


# Calculates fitness
def calculate_fitness(gene_list, rotation_list, rectangles, max_strip_width, it_rotates):
    list_of_heights = []
    list_of_strips = []
    strip = []
    heights = []
    space_used = 0;
    for i in gene_list:

        if it_rotates and rotation_list[i] == 1:
            # rectangle rotates 90 degrees
            rectangle_width = rectangles[i].height
            rectangle_height = rectangles[i].width
        else:
            rectangle_width = rectangles[i].width
            rectangle_height = rectangles[i].height


        # the rectangles widths can not be greater than max_strip_width
        if max_strip_width <= (space_used + rectangle_width):


            if len(heights) == 0 and rectangle_width == max_strip_width:
               list_of_heights.append([rectangle_height])
               list_of_strips.append([i])
            else:
               if len(heights) == 0 and rectangle_width < max_strip_width:
                 heights.append(rectangle_height)
                 strip.append(i)
               else:
                 list_of_heights.append(heights.copy())
                 list_of_strips.append(strip.copy())
                 strip = []
                 heights = []
                 heights.append(rectangle_height)
                 strip.append(i)

            # because we are in a new strip the space used is equal to the only rectangle's width in it. this being the value of rectangle_width
            space_used = rectangle_width
        else:
            # accumulates the widths of the rectangles of one strip because it's lower than W and there is still space left.
            space_used = space_used + rectangle_width
            heights.append(rectangle_height)
            strip.append(i)

    # List of heights.
    list_of_heights.append(heights.copy())

    list_of_strips.append(strip.copy())
    # Sum all height in each strip
    # The lower the better
    sum_of_max_heights = 0
    for items in list_of_heights:
        maximum_height = max(items)
        sum_of_max_heights = sum_of_max_heights + maximum_height

    return sum_of_max_heights
