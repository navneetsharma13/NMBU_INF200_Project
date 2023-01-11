"""
Landscape Class and subclasses (Lowland, Highland, Desert and Water).
Landscape class is a parent class, all objects are instantiated from the
Lowland, Highland, Desert and Water subclasses
"""

from ..animal import carnivore,herbivore

class Landscape():

    def __init__(self):
        """Constructor for the landscape cells."""
        self.initial_population={'Herbivore':[],'Carnivore':[]}
        self.population_to_add={'Herbivore':[],'Carnivore':[]}
        self.fodder=0

    def add_animal(self,animal):
        key=animal.__class__.__name__
        self.initial_population[key].append(animal)

    def sort_by_fitness(self):