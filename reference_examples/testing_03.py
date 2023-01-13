import textwrap
from biosim.simulation import BioSim

geogr = """\
           WWW
           WLW
           WWW"""
geogr = textwrap.dedent(geogr)

ini_herbs = [{'loc': (2, 2),
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(50)]}]


for seed in range(100, 200):
    sim = BioSim(geogr, ini_herbs, seed=seed, vis_years=0,
                 log_file=f'data/mono_hc_{seed:05d}.csv')
    #sim.simulate(50)
    sim.simulate(251)