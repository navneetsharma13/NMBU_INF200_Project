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

    def __init__(self,island_map):

        self.cell_list = self.cell_list(island_map)
        self.cells_dict = self.create_cells()

    def cell_list(self,island_map):
        cells_list = textwrap.dedent(island_map).splitlines()
        return [list(row.strip()) for row in cells_list]

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

    def add_population(self, given_population):

        for population in given_population:

            location = (int(population['loc'][0]) - 1, int(population['loc'][1]) - 1)
            loc_object = self.cells_dict[location]
            for population_individual in population['pop']:

                type_animal = population_individual['species']
                age_weight = (population_individual['age'], population_individual['weight'])
                pop_object = self.animal_classes[type_animal](*age_weight)
                # print(pop_object,pop_object.weight,pop_object.age)
                loc_object.initial_population[type(pop_object).__name__].append(pop_object)

    def check_str_type(self,ar):
        if not isinstance(ar,str):
            raise TypeError("The Argument is not a string "+str(ar))
    def check_dict_type(self,ar):
        if not isinstance(ar,dict):
            raise TypeError("The Argument is not a dict "+str(ar))

    def set_parameters(self,key,params):

        self.check_str_type(key)
        self.check_dict_type(params)
        combined_dict = dict(**self.animal_classes, **self.landscape_classes)
        combined_dict[key].set_parameters(params)


    def yearly_cycle(self):

        for loc, loc_object in self.livable_cell_calculate().items():

            loc_object.add_newborn()
            loc_object.fodder_grow_and_feeding()
            loc_object.age_increase()
            loc_object.weight_decrease()
            loc_object.animal_die()

    def get_pop_tot_num_herb(self):

        herbivore_count = 0
        pop = {'Row_no': [], 'Col_no': [], 'Herbivore': [],
               'Carnivore': []}
        for loc, loc_object in self.cells_dict.items():

            pop['Row_no'].append(loc[0])
            pop['Col_no'].append(loc[1])
            pop['Herbivore'].append(
                len(loc_object.initial_population['Herbivore']))
            pop['Carnivore'].append(
                len(loc_object.initial_population['Carnivore']))

            herbivore_count = sum(pop["Herbivore"])
        return herbivore_count

    def get_pop_tot_num_carn(self):

        carnivore_count = 0
        pop = {'Row_no': [], 'Col_no': [], 'Herbivore': [],
               'Carnivore': []}
        for loc, loc_object in self.cells_dict.items():

            pop['Row_no'].append(loc[0])
            pop['Col_no'].append(loc[1])
            pop['Herbivore'].append(
                len(loc_object.initial_population['Herbivore']))
            pop['Carnivore'].append(
                len(loc_object.initial_population['Carnivore']))

            carnivore_count = sum(pop["Carnivore"])
        return carnivore_count
