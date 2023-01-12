
from src.biosim.map import Map
import textwrap


if __name__ == "__main__":
    geogr = """\
           WWW
           WLW
           WWW"""
    ini_herbs = [{'loc': (2, 2),
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(50)]}]
    m=Map(geogr)
    print(m.create_cells())
    print(m.livable_cell_calculate())
    print(m.add_population(ini_herbs))
    print(m.yearly_cycle())
    print(m.get_pop_tot_num())




