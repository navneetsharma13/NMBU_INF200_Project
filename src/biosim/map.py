from .landscapes import lowland,highland,desert,water
from .animal import herbivore,carnivore

class Map:
    def __init__(self,island_map):
        self._map=island_map
        self._landscape_classes={
            'H':highland,
            'L':lowland,
            'D':desert,
            'W':water
        }
        self._animal_classes={'Carnivore':carnivore,
                              'Herbivore':herbivore

        }

    def _create_cell(self):
