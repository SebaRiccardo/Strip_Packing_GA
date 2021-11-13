
class Individual:

    def __init__(self, gene_list, rotation, max_width, rectangles, fitness_function, it_rotates):
        self.gene_list = gene_list
        self.rotation = rotation
        self.fitness = fitness_function(self.gene_list, self.rotation, rectangles, max_width, it_rotates)

    def __str__(self):
        return "Chromosome: " + str(self.gene_list) + " Fitness: " + str(self.fitness) + " Rotation: " + str(self.rotation)

    def get_gene_list(self):
        return self.gene_list

    def get_rotation(self):
        return self.rotation

    def get_fitness(self):
        return self.fitness
