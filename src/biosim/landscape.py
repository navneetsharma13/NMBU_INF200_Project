
"""
This is the landscape model which functions with the Biosim package written for
the INF200 project January 2023.
"""

__author__ = "Navneet Sharma and Sushant Kumar Srivastava"
__email__ = "navneet.sharma@nmbu.no and sushant.kumar.srivastava@nmbu.no"

import random


class Landscape:
    """
    Landscape Class and its subclasses (Lowland, Highland, Desert and Water). Landscape class is a
    parent class, all objects are instantiated from the Lowland, Highland, Desert and Water
    subclasses

    """
    parameters = {}

    def __init__(self):
        """Constructor for the landscape cells."""
        self.initial_population = {'Herbivore': [], 'Carnivore': []}
        self.after_migration_population = {'Herbivore': [], 'Carnivore': []}
        self.fodder = 0

    @classmethod
    def verify_parameters(cls, params):
        """This method verifies for any wrong parameters passed by the user and raises a ValueError,
         if required.

        Parameters:
        ------------
            params: list
                List with the landscape's parameters.

        Raises:
        ----------
        ValueError
        """
        for parameter in params.keys():
            if parameter not in cls.parameters.keys():
                raise ValueError("Wrong parameter provided: "
                                 "*{}*".format(parameter))

    @classmethod
    def verify_non_valid_parameters(cls, param_key, params):
        """This method verifies for any invalid parameters passed by the user and raises
        a ValueError, if required.

        Parameters:
        ------------
            params: list
                    List with the landscape's parameters.
                    str
                    Param_key.

        Raises:
        ----------
        ValueError

        """
        if isinstance(params[param_key], str) or params[param_key] < 0:
            raise ValueError("The parameter *{}* must be "
                             "non-negative and also not string".format(param_key))

    @classmethod
    def set_parameters(cls, params):
        """This method sets the parameter for the landscape types.

        Parameter:
        ------------
            params: list
                List with the landscape's parameters.
        """
        cls.verify_parameters(params)
        cls.verify_non_valid_parameters('f_max', params)
        cls.parameters.update(params)

    def feed_herbivore(self):
        """This method describes how the herbivores eat the fodder:

        Applied Formulas & Conditions:
        -------------------------------
            'F': Animal's Capacity to eat;
            'f': Available amount of fodder.
            if 'F' <= 'f', then the animal eats 'F';
            elif 0 < 'f' < 'F', then the animal eats 'f';
            elif 'f' = 0, then the animal does not eat.
        """
        random.shuffle(self.initial_population['Herbivore'])
        for herbivore in self.initial_population['Herbivore']:
            fodder_intake = 0
            herb_capacity = herbivore.parameters["F"]
            fodder_remaining = self.fodder
            if fodder_intake >= herb_capacity:
                continue
            elif herb_capacity <= fodder_remaining:
                fodder_intake += herb_capacity
                fodder_remaining -= herb_capacity
            elif 0 < fodder_remaining < herb_capacity:
                fodder_remaining = 0
                fodder_intake += fodder_remaining
            herbivore.weight_increase_on_eat(fodder_intake)
            self.fodder = fodder_remaining

    def feed_carnivore(self):
        """This method organizes the population of carnivore in order
           of descending fitness values. Then, we sort the population of herbivore in order of
           increasing fitness that will be eaten by carnivores. Now, for each carnivore, it is
           applied the carnivore eating criteria, as given below:

        Formula and conditions:
        ------------------------
        Carnivores prey on herbivores on Lowland, Highland and Desert landscapes, and do not
        prey on each other;
        One carnivore tries to kill one herbivore per time, beginning with the herbivore with
        the lowest fitness, and then to the next herbivore until has eaten an amount 'F' of
        herbivore weight;
        The probability to kill a herbivore is given by the method 'kill_prob()';
        The carnivore weight increases by the method 'weight_increase_on_eat()' which also
        updates its fitness;
        Every herbivore killed is removed from the population by the python's built-in
        method '.remove()'.

        """

        self.initial_population['Carnivore'].sort(key=lambda h: h.fitness, reverse=True)

        self.initial_population['Herbivore'].sort(key=lambda h: h.fitness)

        for carnivore in self.initial_population['Carnivore']:
            carn_capacity = carnivore.parameters['F']
            food_intake = 0

            for herbivore in self.initial_population['Herbivore']:

                if food_intake >= carn_capacity:
                    break

                elif carnivore.kill_prob(herbivore.fitness):
                    food_to_eat = carn_capacity - food_intake

                    if herbivore.weight <= food_to_eat:
                        food_intake += herbivore.weight
                        self.initial_population['Herbivore'].remove(herbivore)

                    elif herbivore.weight > food_to_eat:
                        food_intake += food_to_eat
                        self.initial_population['Herbivore'].remove(herbivore)

            carnivore.weight_increase_on_eat(food_intake)

    def add_newborn(self):

        """This method extend a newborn animal population for each specie by adding their
        offspring.
        """

        for specie_type, animals in self.initial_population.items():
            newborns = []
            for animal in animals:
                if animal.birth_prob(len(animals)):
                    newborn = type(animal)()
                    if animal.weight_decrease_on_birth(newborn):
                        newborns.append(newborn)
            self.initial_population[specie_type].extend(newborns)

    def reset_animals(self):
        """This method resets the migration flag after a cycle of one year.
        """

        for species in self.initial_population.values():
            for animals in species:
                animals.has_migrated = False

    def animal_migrate(self, neighbours):
        """ This method iterates through each animal in the cell and runs migrate process.
        Animals will only migrate once per year using the flag `has_migrated` property.

        Parameters
        ------------
        neighbours : dict
        """

        for migrating_specie, animals in self.initial_population.items():

            if len(neighbours) > 0 and len(animals) > 0:

                not_migrated_animal = []
                for animal in animals:

                    if not animal.has_migrated and animal.move_prob():

                        dest_cell = random.choice(neighbours)
                        if str(type(dest_cell)) == "<class 'biosim.landscape.Water'>":
                            not_migrated_animal.append(animal)
                            continue
                        else:
                            dest_cell.after_migration_population[migrating_specie].append(animal)
                    else:
                        not_migrated_animal.append(animal)
                self.initial_population[migrating_specie] = not_migrated_animal
        self.reset_animals()

    def add_migrated_population(self):
        """This method adds the migrated animals to the population of each landscape cell, according
         to its specie type, and empty the list in 'after_migration_population'.
         """
        for specie_type in self.initial_population.keys():
            migrated_animals = self.after_migration_population[specie_type]
            self.initial_population[specie_type].extend(migrated_animals)
            self.after_migration_population[specie_type] = []

    def age_increase(self):
        """This method increase the age of all animals after a cycle of one year.
        """
        for species in self.initial_population.values():
            for animal in species:
                animal.age_increase()

    def weight_decrease(self):
        """This method decreases the weight all animals after a cycle of one year.
        """
        for species in self.initial_population.values():
            for animal in species:
                animal.weight_decrease()

    def animal_die(self):
        """This method only keeps the animal which can survive for next year on the basis
         of die probability.
         """

        for specie_type in self.initial_population.keys():
            living_animal = []
            for animal in self.initial_population[specie_type]:
                if not animal.die_prob():
                    living_animal.append(animal)
            self.initial_population[specie_type] = living_animal


class Lowland(Landscape):
    """
    This Lowland is a subclass/child-class of the Landscape. The Lowland landscape cells offer
    fodder with f_max = 800 for Herbivores and Carnivores can prey on Herbivore in this cell.
    """

    parameters = {'f_max': 800.0}

    def __init__(self):
        """Constructor for the Lowland.
        """

        super().__init__()
        self.fodder = self.parameters['f_max']

    def fodder_grow_and_feeding(self):
        """This method increases the amount of fodder growth from the previous year to now and then
         calls the methods 'feed_herbivore()' and 'feed_carnivore()', respectively, in order to
          execute the animals eating conditions and rules.

        Formula and conditions:
        -------------------------
            The yearly amount of fodder in the Lowland landscape cells is always restored to
             the max ('f_max'):

            'f' = 'f_max'

            where :
            'f_max': The maximum possible amount of fodder in the landscape;
            'f': The remainder available amount of fodder from previous year.
        """

        self.fodder = self.parameters['f_max']
        self.feed_herbivore()
        self.feed_carnivore()


class Highland(Landscape):
    """The Highland is a subclass of the  Landscape. The Highland landscape offer fodder with
    f_max = 800 for Herbivores and Carnivores can prey on Herbivore in this cell.
    """

    parameters = {'f_max': 300.0}

    def __init__(self):
        """Constructor for the Highland.
        """
        super().__init__()
        self.fodder = self.parameters['f_max']

    def fodder_grow_and_feeding(self):
        """This method increases the amount of fodder growth from the previous year to now and then
         calls the methods 'feed_herbivore()' and 'feed_carnivore()', respectively, in order to
         execute the animals eating conditions and rules.

        Formula and conditions:
        ------------------------
            The yearly amount of fodder in the Lowland landscape cells is always restored to
             the max ('f_max'):

            'f' = 'f_max'

            where :
            'f_max': The maximum possible amount of fodder in the landscape;
            'f': The remainder available amount of fodder from previous year.
        """
        self.fodder = self.parameters['f_max']
        self.feed_herbivore()
        self.feed_carnivore()


class Desert(Landscape):
    """The Desert is a subclass of the landscape that can receives animals, but there is no fodder
    available for the Herbivores to eat. But Carnivores can prey on Herbivore in this cell.
    """

    def __init__(self):
        """Constructor for the desert.
        """

        super().__init__()

    def fodder_grow_and_feeding(self):
        """This method increases the amount of fodder growth,
        although, for desert landscape cells, there is no fodder
        growth, then fodder is always equal to zero.
        """

        self.fodder = 0
        self.feed_herbivore()
        self.feed_carnivore()


class Water(Landscape):
    """The Water is a subclass of the landscape type cell and it a passive cell because, in this
    project,the landscape water does not receive the animals, neither Herbivore nor Carnivore.
    """

    def __init__(self):
        """Constructor for the ocean.
        """

        super().__init__()
