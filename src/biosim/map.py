import textwrap
from biosim.landscape import Lowland, Highland, Desert, Water
from biosim.fauna import Herbivore, Carnivore


def geo_list(island_map):
    cells_list = textwrap.dedent(str(island_map)).splitlines()
    return [list(row.strip()) for row in cells_list]


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

        self.cell_list = geo_list(island_map)
        self.cells_dict = self.create_cells()
        self.herb_pop_matrix=[[0 for _ in self.unique_colums()] for _ in self.unique_rows()]
        self.carn_pop_matrix=[[0 for _ in self.unique_colums()] for _ in self.unique_rows()]

    def update_pop_matrix(self):
        for row in self.unique_rows()[1:-1]:  # First and last cell is water
            for col in self.unique_colums()[1:-1]:  # First and last cell is water
                    # print(cell)
                    self.herb_pop_matrix[row - 1][col - 1] = self.get_pop_tot_num_herb()
                    self.carn_pop_matrix[row - 1][col - 1] = self.get_pop_tot_num_carn()


    def create_cells(self):

        pos = [(i, j) for i in range(len(self.cell_list))
               for j in range(len(self.cell_list[0]))]
        geo = [self.landscape_classes[geo]() for k in range(len(self.cell_list))
               for geo in self.cell_list[k]]
        return dict(zip(pos, geo))

    def livable_cell_calculate(self):

        loc = []
        loc_object = []
        for loc1, loc_object1 in self.cells_dict.items():
            if type(loc_object1) in self.livable_cells.values():
                loc.append(loc1)
                loc_object.append(loc_object1)
        return dict(zip(loc, loc_object))

    def migrate_cell_calculate(self):

        loc = []
        loc_object = []
        for loc1, loc_object1 in self.cells_dict.items():
            if type(loc_object1) in self.landscape_classes.values():
                loc.append(loc1)
                loc_object.append(loc_object1)
        return dict(zip(loc, loc_object))

    def add_population(self, given_population):

        for population in given_population:

            location = (int(population['loc'][0]) - 1, int(population['loc'][1]) - 1)
            loc_object = self.cells_dict[location]
            for population_individual in population['pop']:
                type_animal = population_individual['species']
                age_weight = (population_individual['age'], population_individual['weight'])
                pop_object = self.animal_classes[type_animal](*age_weight)
                loc_object.initial_population[type(pop_object).__name__].append(pop_object)

    @staticmethod
    def check_str_type(ar):
        if not isinstance(ar, str):
            raise TypeError("The Argument is not a string " + str(ar))

    @staticmethod
    def check_dict_type(ar):
        if not isinstance(ar, dict):
            raise TypeError("The Argument is not a dict " + str(ar))

    def set_parameters(self, key, params):

        self.check_str_type(key)
        self.check_dict_type(params)
        combined_dict = dict(**self.animal_classes, **self.landscape_classes)
        combined_dict[key].set_parameters(params)

    @staticmethod
    def check_invalid_line_length(cell_l):
        length_count = [len(row) for row in cell_l]
        for i in length_count:
            if i is not length_count[0]:
                return True

    @staticmethod
    def check_invalid_boundary(cell_l):
        for i in range(len(cell_l)):
            if cell_l[i][0] != 'W' or cell_l[i][len(cell_l[i]) - 1] != 'W':
                return True

    def check_invalid_character(self, cell_l):
        for line in cell_l:
            for letter in line:
                if letter not in self.landscape_classes.keys():
                    raise ValueError("Invalid Character in the Map!!")

    def yearly_cycle(self):

        for loc, loc_object in self.livable_cell_calculate().items():
            loc_object.add_newborn()
            loc_object.fodder_grow_and_feeding()
            loc_object.animal_migrate(self.adjacent_cells(loc))
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
    def unique_colums(self):
        return list(set([loc[1] for loc in self.create_cells()]))

    def adjacent_cells(self, pos):

        adjacent_pos = [(pos[0], pos[1] - 1), (pos[0] - 1, pos[1]), (pos[0] + 1, pos[1]),
                        (pos[0], pos[1] + 1)]
        neighbours = [self.migrate_cell_calculate()[loc] for loc in adjacent_pos if
                      loc in self.migrate_cell_calculate().keys()]
        return neighbours
