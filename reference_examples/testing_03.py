import textwrap
from biosim.simulation import BioSim
import time

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
geogr = textwrap.dedent(geogr)

ini_herbs = [{'loc': (5, 7),
                  'pop': [{'species': 'Herbivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(150)]}]
ini_carns = [{'loc': (5, 7),
                  'pop': [{'species': 'Carnivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(40)]}]


start_time = time.time()
for seed in range(134, 135):
    sim = BioSim(geogr, ini_herbs, seed=seed, vis_years=1,
                 log_file=f'data/mono_hc_{seed:05d}.csv', total_years=301)

    sim.simulate(51)
    sim.add_population(ini_carns)
    sim.simulate(251)

print("Simulation took "+str(time.time() - start_time)+" seconds!!")