
from GLOBAL import W

class Individual:

    def __init__(self, gene_list, rotation, rectangles, fitness_fuction):
        self.gene_list = gene_list
        self.rotation = rotation
        self.fitness = fitness_fuction(self.gene_list, rectangles, W)

    def __str__(self):
        return "Chromosome:" + str(self.gene_list) + " Fitness:" + str(self.fitness) + " Rotation:" + str(self.rotation)

    def get_gene_list(self):
        return self.gene_list

    def get_rotation(self):
        return self.rotation

    def get_fitness(self):
        return self.fitness