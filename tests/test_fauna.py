import pytest
from biosim.animal import herbivore,carnivore
import numpy as np

class TestFauna:

    def normal_animal_data(self):
        c_params = {'eta': 0.30,
                        'w_birth': 4.0,
                        'sigma_birth': 1.7,
                        'w_half': 10,
                        'phi_age': 0.4,
                        'phi_weight': 0.6,
                        'a_half': 60,
                        'beta': 0.2,
                        'DeltaPhiMax': 11.0,
                        'mu': 0.25,
                        'gamma': 0.6,
                        'zeta': 1,
                        'omega': 0.6
                        }
        h_params = {'eta': 0.30,
                        'w_birth': 2.0,
                        'sigma_birth': 1.5,
                        'w_half': 10,
                        'phi_age': 0.3,
                        'phi_weight': 0.5,
                        'a_half': 40,
                        'beta': 0.3,
                        'mu': 0.3,
                        'gamma': 0.7,
                        'zeta': 1,
                        'omega': 0.3
                        }
        np.random.seed(1)
        carn = carnivore()
        carn.set_given_parameters(c_params)
        np.random.seed(1)
        herb = herbivore()
        herb.set_given_parameters(h_params)
        return carn, herb


