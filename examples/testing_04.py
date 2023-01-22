import textwrap
from biosim.simulation import BioSim
import time

geogr = """\
              WWWWWWWWWWWWWWWWWWWWW
              WHHHHHLLLLWWLLLLLLLWW
              WHHHHHLLLLWWLLLLLLLWW
              WHHHHHLLLLWWLLLLLLLWW
              WWHHLLLLLLLWWLLLLLLLW
              WWHHLLLLLLLWWLLLLLLLW
              WWWWWWWWHWWWWLLLLLLLW
              WHHHHHLLLLWWLLLLLLLWW
              WHHHHHHHHHWWLLLLLLWWW
              WHHHHHDDDDDLLLLLLLWWW
              WHHHHHDDDDDLLLLLLLWWW
              WHHHHHDDDDDLLLLLLLWWW
              WHHHHHDDDDDWWLLLLLWWW
              WHHHHDDDDDDLLLLWWWWWW
              WWHHHHDDDDDDLWWWWWWWW
              WWHHHHDDDDDLLLWWWWWWW
              WHHHHHDDDDDLLLLLLLWWW
              WHHHHDDDDDDLLLLWWWWWW
              WWHHHHDDDDDLLLWWWWWWW
              WWWHHHHLLLLLLLWWWWWWW
              WWWHHHHHHWWWWWWWWWWWW
              WWWWWWWWWWWWWWWWWWWWW"""
geogr = textwrap.dedent(geogr)

ini_herbs = [{'loc': (2, 7),
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(200)]}]
ini_carns = [{'loc': (2, 7),
              'pop': [{'species': 'Carnivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(50)]}]

start_time = time.time()
for seed in range(100, 101):
    sim = BioSim(geogr, ini_herbs + ini_carns, hist_specs={'fitness': {'max': 1.0, 'delta': 0.05},
                                                           'age': {'max': 60.0, 'delta': 2},
                                                           'weight': {'max': 60, 'delta': 2}},
                 plot_graph=True,
                 cmax_animals={'Herbivore': 200, 'Carnivore': 50}, seed=seed,
                 vis_years=1, img_years=1,total_years=401)

    sim.simulate(400)

print("Simulation took " + str(time.time() - start_time) + " seconds!!")
