from src.biosim.simulation import BioSim
from src.biosim.map import Map
from src.biosim.landscape import Landscape
import textwrap


if __name__ == "__main__":
    geogr = """\
           WWW
           WLW
           WWW"""
    ini_herbs = [{'loc': (2, 3),
              'pop': [{'species': 'Herbivore',
                       'age': 3,
                       'weight': 5}
                      for _ in range(50)]},
                 {'loc': (1, 1),
              'pop': [{'species': 'Carnivore',
                       'age': 15,
                       'weight': 10}
                      for _ in range(50)]}]
    seed = 123413
    t_sim = BioSim(geogr, ini_herbs, seed)
    m = Map(geogr)
    l = Landscape()
    m.create_cells()
    m.add_population(ini_herbs)
    print(m.get_pop_age_herb())
    print(m.get_pop_age_carn())
    print(m.get_pop_weight_herb())
    print(m.get_pop_weight_carn())
    print(m.get_pop_fitness_herb())
    print(m.get_pop_fitness_carn())
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





