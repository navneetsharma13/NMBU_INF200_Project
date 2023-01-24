from src.biosim.simulation import BioSim

if __name__ == "__main__":
    geogr = """\
           WWWWW
           WLWWW
           WWWWW"""
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
