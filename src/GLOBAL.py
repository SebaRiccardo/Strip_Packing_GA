
# genes lo uso solo como parametro para determinar la longitud
# de los arreglos que hacen de lista de genes, en caso de aumentar la cantidad de rectangulos
# se debe aumentar el arrelgo, el orden es indistinto solo es necesario que tenga la longitud adecuada
# ej: num de rectangulos = 3 [1,2,3]  o [3,2,1] o [3,1,2]. Cualquiera sirve ya que despues np.permutation() permuta
# y crea las distintas variantes de los genes

RECTANGLES_NUMBER = 15
RESULTS_FOLDER = "results"
TOURNAMENT_SIZE = 5
POPULATION_SIZE = 50
MAX_GENERATIONS = 500
MUTATION_PROBABILITY = .1
CROSS_OVER_PROBABILITY = .65
MAX_WIDTH = 100

instances = {
        "Instance 1": "spp9a.txt",
        "Instance 2": "spp9b.txt",
        "Intances 3": "spp10.txt",
        "Intances 4": "spp11.txt",
        "Intances 5": "spp12.txt",
        "Intances 6": "spp13.txt"
    }
