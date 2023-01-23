import textwrap
from biosim.landscape import Lowland, Highland, Desert, Water
from biosim.fauna import Herbivore, Carnivore


class Map:
    landscape_classes = {
        'H': Highland,
        'L': Lowland,
        'D': Desert,
        'W': Water
    }
    animal_classes = {'Carnivore': Carnivore, 'Herbivore': Herbivore
                      }
    livable_cells = {'H': Highland, 'L': Lowland, 'D': Desert}

    def __init__(self, island_map):

        self.island_map = island_map
        self.cell_list = self.geo_list()
        self.check_invalid_map()
        self.herb_pop_matrix = [[0 for _ in self.unique_columns()] for _ in self.unique_rows()]
        self.carn_pop_matrix = [[0 for _ in self.unique_columns()] for _ in self.unique_rows()]
        self.cells_dict = self.create_cells()
        self.neighbours_dict = self.create_neighbours_dict()

    def geo_list(self):
        cells_list = textwrap.dedent(str(self.island_map)).splitlines()
        return [list(row.strip()) for row in cells_list]

    def check_invalid_map(self):

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
        if not isinstance(ar, dict):
            raise TypeError("The Argument is not a dict " + str(ar))

    def set_parameters(self, key, params):

        self.check_dict_type(params)
        combined_dict = dict(**self.animal_classes, **self.landscape_classes)
        combined_dict[key].set_parameters(params)

    def check_invalid_character(self, cell_l):
        for line in cell_l:
            for letter in line:
                if letter not in self.landscape_classes.keys():
                    raise ValueError("Invalid Character in the Map!!")

    def create_cells(self):

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

            if type(loc_object1) in self.livable_cells.values():
                m_loc.append(loc1)
                migrate_loc_object.append(loc_object1)

        return dict(zip(loc, loc_object)), dict(zip(m_loc, migrate_loc_object))

    def livable_cell_calculate(self):

        livable_cells, _ = self.find_cell_object()
        return livable_cells

    def migrate_cell_calculate(self):

        _, migrate_cells = self.find_cell_object()
        return migrate_cells

    def create_neighbours_dict(self):

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

        for population in given_population:

            location = (int(population['loc'][0]) - 1, int(population['loc'][1]) - 1)
            loc_object = self.cells_dict[location]
            for population_individual in population['pop']:
                type_animal = population_individual['species']
                age_weight = (population_individual['age'], population_individual['weight'])
                pop_object = self.animal_classes[type_animal](*age_weight)
                loc_object.initial_population[type(pop_object).__name__].append(pop_object)

    def yearly_cycle(self):

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

        pop = self.calculate_animal_count()
        return sum(pop["Herbivore"])

    def get_pop_tot_num_carn(self):

        pop = self.calculate_animal_count()
        return sum(pop["Carnivore"])

    def get_pop_tot_num(self):

        pop = self.calculate_animal_count()
        return sum(pop["Carnivore"]) + sum(pop["Herbivore"])

    def unique_rows(self):
        return list(set([loc[0] for loc in self.create_cells()]))

    def unique_columns(self):
        return list(set([loc[1] for loc in self.create_cells()]))

    def get_pop_matrix_herb(self):
        pos = 0
        for row in (self.unique_rows()):
            for col in (self.unique_columns()):
                self.herb_pop_matrix[row][col] = self.calculate_animal_count()['Herbivore'][pos]
                pos += 1

        return self.herb_pop_matrix

    def get_pop_matrix_carn(self):
        pos = 0
        for row in (self.unique_rows()):
            for col in (self.unique_columns()):
                self.carn_pop_matrix[row][col] = self.calculate_animal_count()['Carnivore'][pos]
                pos += 1

        return self.carn_pop_matrix

    def get_pop_age_herb(self):
        herb_age = []
        for loc, loc_object in self.cells_dict.items():
            for animal in loc_object.initial_population['Herbivore']:
                herb_age.append(animal.age)
        return herb_age

    def get_pop_age_carn(self):
        carn_age = []
        for loc, loc_object in self.cells_dict.items():
            for animal in loc_object.initial_population['Carnivore']:
                carn_age.append(animal.age)
        return carn_age

    def get_pop_weight_herb(self):
        herb_weight = []
        for loc, loc_object in self.cells_dict.items():
            for animal in loc_object.initial_population['Herbivore']:
                herb_weight.append(animal.weight)
        return herb_weight

    def get_pop_weight_carn(self):
        carn_weight = []
        for loc, loc_object in self.cells_dict.items():
            for animal in loc_object.initial_population['Carnivore']:
                carn_weight.append(animal.weight)
        return carn_weight

    def get_pop_fitness_herb(self):
        herb_fitness = []
        for loc, loc_object in self.cells_dict.items():
            for animal in loc_object.initial_population['Herbivore']:
                animal.calculate_fitness()
                herb_fitness.append(animal.fitness)
        return herb_fitness

    def get_pop_fitness_carn(self):
        carn_fitness = []
        for loc, loc_object in self.cells_dict.items():
            for animal in loc_object.initial_population['Carnivore']:
                animal.calculate_fitness()
                carn_fitness.append(animal.fitness)
        return carn_fitness
