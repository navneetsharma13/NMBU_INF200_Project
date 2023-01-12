"""
Landscape Class and subclasses (Lowland, Highland, Desert and Water).
Landscape class is a parent class, all objects are instantiated from the
Lowland, Highland, Desert and Water subclasses
"""
import random

from .fauna import Herbivore, Carnivore


class Landscape:
    parameters = {}

    def __init__(self, herb_num, carn_num):
        """Constructor for the landscape cells."""
        self.initial_population = {'Herbivore': [Herbivore() for _ in range(herb_num)],
                                   'Carnivore': [Carnivore() for _ in range(carn_num)]}
        # self.initial_population = {'Herbivore': [], 'Carnivore': []}
        self.population_to_add = {'Herbivore': [], 'Carnivore': []}
        self.fodder = 0

    @classmethod
    def verify_parameters(cls, params):
        """This method verifies for any wrong parameters
        passed by the user and raises a
        ValueError, if required.

        Parameters:
        ----------
            params: list
                List with the landscape's parameters.
        """
        for parameter in params.keys():
            if parameter not in cls.parameters.keys():
                raise ValueError("Wrong parameter provided: "
                                 "*{}*".format(parameter))

    @classmethod
    def verify_non_valid_parameters(cls, param_key, params):
        if params[param_key] < 0 or isinstance(params[param_key], str):
            raise ValueError("The parameter *{}* must be "
                             "non-negative and also not string".format(param_key))

    @classmethod
    def set_parameters(cls, params):
        """This method sets the parameter for the landscape types.

        Parameter:
        ----------
            params: list
                List with the landscape's parameters.
        """
        cls.verify_parameters(params)
        cls.verify_non_valid_parameters('f_max', params)
        cls.parameters.update(params)

    def feed_herbivore(self):
        """This method describes how the herbivores eat the fodder:

                Applied Formulas & Conditions:
                ----------
                    -> 'F': Animal's Capacity to eat;
                    -> 'f': Available amount of fodder.
                    -> if 'F' <= 'f', then the animal eats 'F';
                    -> elif 0 < 'f' < 'F', then the animal eats 'f';
                    -> elif 'f' = 0, then the animal does not eat.
                """
        random.shuffle(self.initial_population['Herbivore'])
        for herbivore in self.initial_population['Herbivore']:
            fodder_intake = 0
            herb_capacity = herbivore.parameters["F"]
            fodder_remaining = self.fodder
            if herb_capacity <= fodder_remaining:
                fodder_intake += herb_capacity
                fodder_remaining -= herb_capacity
            elif 0 < fodder_remaining < herb_capacity:
                fodder_remaining = 0
                fodder_intake += fodder_remaining
            herbivore.weight_increase_on_eat(fodder_intake)
            self.fodder = fodder_remaining

    def add_newborn(self):
        """This method extend a newborn animal population for each specie by adding their
        offspring."""
        for species in self.initial_population.values():
            newborns = []
            for animal in species:
                if animal.birth_prob(len(species)):
                    newborn = type(animal)()
                    animal.weight_decrease_on_birth(newborn)
                    newborns.append(newborn)
            species.extend(newborns)

    def age_increase(self):
        for species in self.initial_population.values():
            for animal in species:
                animal.age_increase()

    def weight_decrease(self):
        for species in self.initial_population.values():
            for animal in species:
                animal.weight_decrease()

    def animal_die(self):
        for specie_type in self.initial_population.keys():
            living_animal = []
            for animal in self.initial_population[specie_type]:
                if not animal.die_prob():
                    living_animal.append(animal)
            self.initial_population[specie_type] = living_animal


class Lowland(Landscape):
    """
    This Lowland is a subclass/child-class of the Landscape. The Lowland landscape cells offer
    fodder with f_max = 800 for Herbivores and Carnivores can prey on Herbivore in this cell.c"""

    parameters = {'f_max': 800.0}

    def __init__(self, herb_num=None, carn_num=None):
        """Constructor for the Lowland."""
        super().__init__(herb_num, carn_num)
        self.fodder = self.parameters['f_max']

    def fodder_grow_and_feeding(self):
        self.fodder = self.parameters['f_max']
        self.feed_herbivore()
        # self.feed_carnivore()


class Highland(Landscape):
    """The Highland is a subclass of the  Landscape. The Highland landscape offer fodder with
    f_max = 800 for Herbivores and Carnivores can prey on Herbivore in this cell."""
    parameters = {'f_max': 300.0}

    def __init__(self, herb_num=None, carn_num=None):
        """Constructor for the Highland."""
        super().__init__(herb_num, carn_num)
        self.fodder = self.parameters['f_max']

    def grow_fodder_and_feed(self):
        self.fodder = self.parameters['f_max']
        self.feed_herbivore()
        # self.feed_carnivore()


class Desert(Landscape):
    """The Desert is a subclass of the landscape that can receives animals, but there is no fodder
    available for the Herbivores to eat. But Carnivores can prey on Herbivore in this cell."""

    def __init__(self, herb_num=None, carn_num=None):
        """Constructor for the desert."""
        super().__init__(herb_num, carn_num)

    def grow_fodder_and_feed(self):
        """This method increases the amount of fodder growth,
        although, for desert landscape cells, there is no fodder
        growth, then fodder is always equal to zero."""
        self.fodder = 0
        self.feed_herbivore()
        # self.feed_carnivore()


class Water(Landscape):
    """The Water is a subclass of the landscape type cell and it a passive cell because, in this
    project,the landscape water does not receive the animals, neither Herbivore nor Carnivore."""

    def __init__(self, herb_num=None, carn_num=None):
        """Constructor for the ocean."""
        super().__init__(herb_num, carn_num)
