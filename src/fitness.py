import numpy as np
from utils import strip_width

# Calculates fitness
def calculate_fitness(gene_list, rotation_list, rectangles, max_strip_width,it_rotates):

        list_of_heights = []
        heights = np.array([])
        sum_of_widths = 0;

        for i in gene_list:

            rectangle_width=0
            rectangle_height=0

            if it_rotates and rotation_list[i]==1:
                #rectangle rotates 90 degrees
                rectangle_width = rectangles[i].height
                rectangle_height = rectangles[i].width
            else:
                rectangle_width = rectangles[i].width
                rectangle_height = rectangles[i].height

            # the rectangles widths can not be greater than W
            if max_strip_width <= (sum_of_widths + rectangle_width):
                # One strip is already complete and will overflow the maximun width W.
                # copy the heights for the current strip into a list of heights.
                aux = np.copy(heights)
                list_of_heights.append(aux)
                heights = []
                # it adds the width of the rectangle in the new strip
                sum_of_widths = rectangle_width
            else:
                # accumulates the widths of the rectangles of one strip because it's lower than W
                sum_of_widths = sum_of_widths + rectangle_width

            heights = np.append(heights, rectangle_height)
        # List of heights.
        list_of_heights.append(heights)

        # Sum all height in each strip
        # The lower the better
        sum_of_max_heights = 0
        for items in list_of_heights:
            maximun_height = max(items)
            sum_of_max_heights = sum_of_max_heights + maximun_height
        return sum_of_max_heights
