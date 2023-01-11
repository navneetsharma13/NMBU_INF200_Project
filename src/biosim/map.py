import textwrap

from .landscape import lowland,highland,desert,water
from .animal import herbivore,carnivore

class Map:
    landscape_classes={
            'H':highland,
            'L':lowland,
            'D':desert,
            'W':water
        }
    animal_classes={'Carnivore':carnivore,'Herbivore':herbivore
                    }
    livable_cells={'H':highland,'L':lowland}
    def __init__(self,island_map):
        self.map=self.string_to_list_cells(island_map)
        landscape_classes={
            'H':highland,
            'L':lowland,
            'D':desert,
            'W':water
        }
        animal_classes={'Carnivore':carnivore,
                              'Herbivore':herbivore

        }
        self.cells=self.create_cells()
    def create_cells(self):


        pos=[(i,j) for i in range(len(self.map))
             for j in range(len(self.map[0]))]
        geo=[self.landscape_classes[geo]() for j in range(len(self.map))
             for geo in self.map[j]]
        return dict(zip(pos,geo))
    def string_to_list_cells(island_map):

        cells_list=textwrap.dedent(island_map).splitlines()
        return [list(row.strip()) for row in cells_list]

    # def livable_cells(self):
    #
    #     loc=[]
    #     loc_object=[]
    #     for loc,loc_objects in self.cells.items():
    #          (loc_object) in self.livable_cells.values():
