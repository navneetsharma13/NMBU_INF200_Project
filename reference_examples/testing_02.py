from src.biosim.simulation import BioSim
from src.biosim.map import Map
from src.biosim.landscape import Landscape
import textwrap


if __name__ == "__main__":
    geogr = """\
               WWWWWWWWWWWWWWWWWWWWW
               WWWWWWWWHWWWWLLLLLLLW
               WHHHHHLLLLWWLLLLLLLWW
               WHHHHHHHHHWWLLLLLLWWW
               WHHHHHLLLLLLLLLLLLWWW
               WHHHHHLLLDDLLLHLLLWWW
               WHHLLLLLDDDLLLHHHHWWW
               WWHHHHLLLDDLLLHWWWWWW
               WHHHLLLLLDDLLLLLLLWWW
               WHHHHLLLLDDLLLLWWWWWW
               WWHHHHLLLLLLLLWWWWWWW
               WWWHHHHLLLLLLLWWWWWWW
               WWWWWWWWWWWWWWWWWWWWW"""
    ini_herbs = [{'loc': (2, 2),
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(50)]}]
    seed = 123413
    t_sim = BioSim(geogr, ini_herbs, seed)
    m = Map(geogr)
    l = Landscape()
    m.add_population(ini_herbs)
    print(m.unique_rows(),m.unique_colums())
    # print(t_sim.map.livable_cell_calculate())
    # print(t_sim.map.adjacent_cells((1,1)))
    # for i in range(10):
    #     print(t_sim.map.livable_cell_calculate()[1, 1].animal_migrate((t_sim.map.adjacent_cells((1, 1)))))
    #     # print(m.geo_list(geogr))
    #     print(m.create_cells())
    #     print(m.add_population(ini_herbs))
    #     print(m.yearly_cycle())
    #     print(m.get_pop_tot_num_herb())
    #     print(m.get_pop_tot_num_carn())
    #print(m.set_parameters("Herbivore",{'w_birth':300}))





