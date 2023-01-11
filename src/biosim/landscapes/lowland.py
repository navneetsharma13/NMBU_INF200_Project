from ..animal import carnivore,herbivore

class Cell():

    def __init__(self):

        self.initial_population={'herbivore':[],'carnivore':[]}
        self.population_to_add={'herbivore':[],'carnivore':[]}
        self.fodder=0

    def add_animal(self,animal):
        key=animal.__class__.__name__
        self.initial_population[key].append(animal)

    def sort_by_fitness(self):










