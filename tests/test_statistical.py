
"""
This is the Test file using statistical tests for some methods in the Biosim package written for
the INF200 project January 2023.
"""

__author__ = "Navneet Sharma and Sushant Kumar Srivastava"
__email__ = "navneet.sharma@nmbu.no and sushant.kumar.srivastava@nmbu.no"

import textwrap
import pytest
from biosim.simulation import BioSim
from scipy import stats


class TestStatistical:
    """
    Checks if the birth weight is following the gaussian distribution.
    """
    @pytest.fixture()
    def test_add_newborn_animal_data(self):
        """
        Generates population of animals and an array of their initial weight to
        be used in test_birth_weight_dist

        Returns
        -------
        newborns: list
            list of animals' initial weight
        """
        geogr = """\
                               WWW
                               WLW
                               WWW"""
        geogr = textwrap.dedent(geogr)

        ini_herbs = [
            {
                "loc": (2, 2),
                "pop": [
                    {"species": "Herbivore", "age": 5, "weight": 40}
                    for _ in range(50)
                ],
            }
        ]

        seed = 23423
        t_sim = BioSim(geogr, ini_herbs, seed)
        loc = (1, 1)
        loc_object = t_sim.map.livable_cell_calculate()[loc]
        newborns = []
        for specie_type, animals in loc_object.initial_population.items():
            for animal in animals:
                if animal.birth_prob(len(animals)):
                    newborn = type(animal)()
                    newborns.append(newborn)
        newborn_weights = []
        for i in range(len(newborns)):
            newborn_weights.append(newborns[i].weight)

        print(newborn_weights)
        return newborn_weights

    def test_birth_weight_dist(self, test_add_newborn_animal_data):
        """
        This method tests if the null hypothesis is rejected or not by comparing the p_value
        if it is less than alpha = 1% or not. Null hypothesis is "test_add_newborn_animal_data
        follows the log-normal distribution"

        Parameters
        -----------
        test_add_newborn_animal_data : list

        """
        birth_weight_list = test_add_newborn_animal_data
        _, p_value = stats.normaltest(birth_weight_list)
        alpha = 0.01
        assert p_value >= alpha
        print("The null hypothesis cannot be rejected, therefore the weights for newborns follows"
              "the log-normal distribution")
