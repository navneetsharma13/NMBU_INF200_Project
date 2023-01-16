import textwrap
from random import seed

from biosim.simulation import BioSim
import time

geogr = """\
           WWW
           WLW
           WWW"""
geogr = textwrap.dedent(geogr)
print(geogr)
ini_herbs = [{'loc': (2, 2),
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(50)]}]

ini_carns = [{'loc': (2, 2),
              'pop': [{'species': 'Carnivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(20)]}]


start_time = time.time()

if __name__ == '__main__':
    sim = BioSim(geogr, ini_herbs, seed=seed)
    sim.run(cycles=20)