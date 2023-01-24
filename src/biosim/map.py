

"""
This is the Map model which functions with the Biosim package written for the INF200 project
January 2023.
"""

__author__ = "Navneet Sharma and Sushant Kumar Srivastava"
__email__ = "navneet.sharma@nmbu.no and sushant.kumar.srivastava@nmbu.no"

import textwrap
from biosim.landscape import Lowland, Highland, Desert, Water
from biosim.fauna import Herbivore, Carnivore


class Map:
    """The Map object collects all landscape cells in the map and keeps track of animals.

    :Example:
        .. code-block:: python

            example_map = '''WWWW
                             WLDW
                             WHDW
                             WWWW'''

    .. note::

        - Only H, L, D and W cell representation are accepted.
        - All map rows need to be the same length.
    """

    # Dict consisting of landscape classes used for migration.
    landscape_classes = {
        'H': Highland,
        'L': Lowland,
        'D': Desert,
        'W': Water
    }
    # Dict consisting of animal classes used for adding population
    animal_classes = {'Carnivore': Carnivore, 'Herbivore': Herbivore
                      }
    # Dict consisting of landscape classes in which animal can live
    livable_cells = {'H': Highland, 'L': Lowland, 'D': Desert}

    def __init__(self, island_map):
        """Constructor for Map class"""
        self.island_map = island_map  # save island_map_str as property
        self.cell_list = self.geo_list()  # storing the island_map str converted to list
        self.check_invalid_map()  # checking for all types of invalid map given as input.
        self.herb_pop_matrix = [[0 for _ in self.unique_columns()] for _ in
                                self.unique_rows()]  # Herbivore population matrix
        self.carn_pop_matrix = [[0 for _ in self.unique_columns()] for _ in
                                self.unique_rows()]  # Carnivore population matrix
        self.cells_dict = self.create_cells()  # storing the dict with coordinates and cells
        self.neighbours_dict = self.create_neighbours_dict()  # storing the dict with neighbours

    def geo_list(self):
        """This method converts island_map str into list with each element corresponding to
        each cell element in the map

        Returns:
        ----------
        List with element as each cell element in map.
        """
        cells_list = textwrap.dedent(str(self.island_map)).splitlines()
        return [list(row.strip()) for row in cells_list]

    def check_invalid_map(self):
        """This method check for various invalid map types given as str.

        Checks for Invalid line lengths.
        Checks for Invalid character.
        Checks for Invalid Edges : has to be water surrounding the map.

        Raises:
        ----------
        ValueError if conditions are met.
        """

        rows, cols = len(self.cell_list), len(self.cell_list[0])
        for i in range(rows):

            if len(self.cell_list[i]) != cols:
                raise ValueError("The given Map is not Valid,The row length is not equal.")

            for k in range(len(self.cell_list[i])):
                if self.cell_list[i][k] not in self.landscape_classes.keys():
                    raise ValueError(
                        "Invalid Character in the Map at pos:" + str(i + 1) + ',' + str(k + 1))

            if self.cell_list[i][0] != 'W':
                raise ValueError(
                    "The given Map is not Valid,The edges of Map has to be Water at pos :" + str(
                        i + 1) + ',' + str(1))

            if self.cell_list[i][cols - 1] != 'W':
                raise ValueError(
                    "The given Map is not Valid,The edges of Map has to be Water at pos :" + str(
                        i + 1) + ',' + str(cols))

            if i == 0 or i == rows - 1:
                cell_l = (self.cell_list[i][:cols])
                for j in range(len(cell_l)):
                    if cell_l[j] != 'W':
                        raise ValueError(
                            "The given Map is not Valid,The edges of Map has to be Water at pos :"
                            + str(
                                i + 1) + ',' + str(j + 1))

    @staticmethod
    def check_dict_type(ar):
        """This method checks if the argument given by the user is a
        dictionary and raises a TypeError if necessary.

        Parameters:
        ------------
            argument: str
        """
        if not isinstance(ar, dict):
            raise TypeError("The Argument is not a dict " + str(ar))

    def set_parameters(self, key, params):
        """This method sets the parameter for the landscapes and animals.

        Parameter:
        ----------
            key: str

            params: list
        """
        self.check_dict_type(params)
        combined_dict = dict(**self.animal_classes, **self.landscape_classes)
        combined_dict[key].set_parameters(params)

    def create_cells(self):
        """This method creates a dictionary with the coordinates on
        keys and landscape objects on values.

        Returns:
        ----------
        dict
        """
        pos = [(i, j) for i in range(len(self.cell_list))
               for j in range(len(self.cell_list[0]))]
        geo = [self.landscape_classes[geo]() for k in range(len(self.cell_list))
               for geo in self.cell_list[k]]
        return dict(zip(pos, geo))

    def find_cell_object(self):

        loc = []
        loc_object = []

        m_loc = []
        migrate_loc_object = []
        for loc1, loc_object1 in self.cells_dict.items():
            if type(loc_object1) in self.livable_cells.values():
                loc.append(loc1)
                loc_object.append(loc_object1)

            if type(loc_object1) in self.landscape_classes.values():
                m_loc.append(loc1)
                migrate_loc_object.append(loc_object1)

        return dict(zip(loc, loc_object)), dict(zip(m_loc, migrate_loc_object))

    def livable_cell_calculate(self):
        """This method creates a dictionary with only the coordinates
        that are livable and store the coordinates on keys and
        landscape objects on values.

        Returns:
        ----------
            dict
        """
        livable_cells, _ = self.find_cell_object()
        return livable_cells

    def migrate_cell_calculate(self):
        """This method creates a dictionary with only the coordinates
        where migration is possible and store the coordinates on keys and
        landscape objects on values.

        Returns:
        ----------
            List of coordinates where migration is possible.
        """
        _, migrate_cells = self.find_cell_object()
        return migrate_cells

    def create_neighbours_dict(self):
        """This method localizes the neighbour cells (north, south,
        west and east), checks if they are livable and returns a
        location of landscape objects.

        Returns:
        ----------
            Dict with neighbours loc as values given for a given loc as key.
        """
        own_loc = []
        neighbours = []
        for loc, _ in self.cells_dict.items():
            own_loc.append(loc)
            neighbour_pos = [(loc[0], loc[1] - 1), (loc[0] - 1, loc[1]),
                             (loc[0] + 1, loc[1]), (loc[0], loc[1] + 1)]
            neighbours_loc = [self.migrate_cell_calculate()[loc] for loc in neighbour_pos if
                              loc in self.migrate_cell_calculate().keys()]
            neighbours.append(neighbours_loc)

        return dict(zip(own_loc, neighbours))

    def add_population(self, given_population):
        """This method creates the population objects inside the
        cells.

        Parameter:
        ----------
            given_pop: list
        """
        for population in given_population:

            location = (int(population['loc'][0]) - 1, int(population['loc'][1]) - 1)
            loc_object = self.cells_dict[location]
            for population_individual in population['pop']:
                type_animal = population_individual['species']
                age_weight = (population_individual['age'], population_individual['weight'])
                pop_object = self.animal_classes[type_animal](*age_weight)
                loc_object.initial_population[type(pop_object).__name__].append(pop_object)

    def yearly_cycle(self):
        """This method calls, in order, the methods that compound
        the yearly cycle dynamics of the island, such that:

            1. Animal's birth;
            2. Animal's feeding;
            3. Animal's migration;
            4. Animal's migration;
            5. Animal's aging;
            6. Animal's weight loss;
            7. Animal's death.
        """
        for loc, loc_object in self.livable_cell_calculate().items():
            loc_object.add_newborn()
            loc_object.fodder_grow_and_feeding()
            loc_object.animal_migrate(self.neighbours_dict[loc])
        for loc, loc_object in self.livable_cell_calculate().items():
            loc_object.add_migrated_population()
            loc_object.age_increase()
            loc_object.weight_decrease()
            loc_object.animal_die()

    def calculate_animal_count(self):
        """This method calculates the distribution of the Herbivore and Carnivore
        and stores into dict along with row and column no.

        Returns:
        ----------
        Dict
        """

        pop = {'Row_no': [], 'Col_no': [], 'Herbivore': [],
               'Carnivore': []}
        for loc, loc_object in self.cells_dict.items():
            pop['Row_no'].append(loc[0])
            pop['Col_no'].append(loc[1])
            pop['Herbivore'].append(
                len(loc_object.initial_population['Herbivore']) +
                len(loc_object.after_migration_population['Herbivore']))
            pop['Carnivore'].append(
                len(loc_object.initial_population['Carnivore']) +
                len(loc_object.after_migration_population['Carnivore']))
        return pop

    def get_pop_tot_num_herb(self):
        """This method calculates the total no of herbivores on an island.

        Returns:
        ----------
        int
        """

        pop = self.calculate_animal_count()
        return sum(pop["Herbivore"])

    def get_pop_tot_num_carn(self):
        """This method calculates the total no of carnivores on an island.

        Returns:
        ----------
        int
        """

        pop = self.calculate_animal_count()
        return sum(pop["Carnivore"])

    def get_pop_tot_num(self):
        """This method calculates the total no of animals on an island.

        Returns:
        ----------
        int
        """

        pop = self.calculate_animal_count()
        return sum(pop["Carnivore"]) + sum(pop["Herbivore"])

    def unique_rows(self):
        """Return unique row values.

        Returns:
        ----------
        list : Row coordinate values

        """
        return list(set([loc[0] for loc in self.create_cells()]))

    def unique_columns(self):
        """Return unique column values.

        Returns:
        ----------
        list : column coordinate values

        """
        return list(set([loc[1] for loc in self.create_cells()]))

    def get_pop_matrix_herb(self):
        """Update the population matrices of herbivore for heatmap.

        :Example:

            .. code-block:: python

                example_matrix = [
                    [0, 0, 0],
                    [0, 221, 0],
                    [0, 0, 0],
                ]

        Returns:
        ----------
        List of list

        """
        pos = 0
        for row in (self.unique_rows()):
            for col in (self.unique_columns()):
                self.herb_pop_matrix[row][col] = self.calculate_animal_count()['Herbivore'][pos]
                pos += 1

        return self.herb_pop_matrix

    def get_pop_matrix_carn(self):
        """Update the population matrices of carnivore for heatmap.

        :Example:

            .. code-block:: python

                example_matrix = [
                    [0, 0, 0],
                    [0, 221, 0],
                    [0, 0, 0],
                ]

        Returns:
        ----------
        List of list

        """
        pos = 0
        for row in (self.unique_rows()):
            for col in (self.unique_columns()):
                self.carn_pop_matrix[row][col] = self.calculate_animal_count()['Carnivore'][pos]
                pos += 1

        return self.carn_pop_matrix

    def get_pop_age_herb(self):

        """This method return the list of all herbivore age used for histogram plot

        Returns:
        ----------
        List

        """
        herb_age = []
        for loc, loc_object in self.cells_dict.items():
            for animal in loc_object.initial_population['Herbivore']:
                herb_age.append(animal.age)
        return herb_age

    def get_pop_age_carn(self):
        """This method return the list of all carnivore age used for histogram plot

        Returns:
        ----------
        List

        """
        carn_age = []
        for loc, loc_object in self.cells_dict.items():
            for animal in loc_object.initial_population['Carnivore']:
                carn_age.append(animal.age)
        return carn_age

    def get_pop_weight_herb(self):
        """This method return the list of all herbivore weight used for histogram plot

        Returns:
        ----------
        List

        """
        herb_weight = []
        for loc, loc_object in self.cells_dict.items():
            for animal in loc_object.initial_population['Herbivore']:
                herb_weight.append(animal.weight)
        return herb_weight

    def get_pop_weight_carn(self):
        """This method return the list of all carnivore weight used for histogram plot

        Returns:
        ----------
        List

        """
        carn_weight = []
        for loc, loc_object in self.cells_dict.items():
            for animal in loc_object.initial_population['Carnivore']:
                carn_weight.append(animal.weight)
        return carn_weight

    def get_pop_fitness_herb(self):
        """This method return the list of all herbivore fitness used for histogram plot

        Returns:
        ----------
        List

        """
        herb_fitness = []
        for loc, loc_object in self.cells_dict.items():
            for animal in loc_object.initial_population['Herbivore']:
                animal.calculate_fitness()
                herb_fitness.append(animal.fitness)
        return herb_fitness

    def get_pop_fitness_carn(self):
        """This method return the list of all carnivore fitness used for histogram plot

        Returns:
        ----------
        List

        """
        carn_fitness = []
        for loc, loc_object in self.cells_dict.items():
            for animal in loc_object.initial_population['Carnivore']:
                animal.calculate_fitness()
                carn_fitness.append(animal.fitness)
        return carn_fitness
