"""
This is the geography pytest package which is a test package for the  BioSim packages written for
 the INF200 project January 2022.
"""

__author__ = "Navneet Sharma and Sushant Kumar Srivastava"
__email__ = "navneet.sharma@nmbu.no and sushant.kumar.srivastava@nmbu.no"

import random
import textwrap
import pytest
from biosim.landscape import Lowland, Highland
from biosim.simulation import BioSim


def test_verify_unknown_parameters():
    """Test method 'verify_parameters()' if it does not identify the given parameter as incorrect
     and return ValueError"""
    with pytest.raises(ValueError):
        Lowland.verify_parameters(params={'f_min': 100})
        Highland.verify_parameters(params={'f_min': 100})


def test_verify_known_parameters():
    """Test method 'verify_parameters()' if it does not identify the given parameter are correct and
     returns ValueError"""
    Lowland.verify_parameters(params={'f_max': 100})
    Highland.verify_parameters(params={'f_max': 100})


def test_negative_parameters():
    """Test method 'verify_non_valid_parameters(param_key, params)' if it identifies the
    negative value of a given parameter and returns ValueError"""
    param_key, params = 'f_max', {'f_max': -344}
    with pytest.raises(ValueError):
        Lowland.verify_non_valid_parameters(param_key, params)
        Highland.verify_non_valid_parameters(param_key, params)


def test_string_parameters():
    """Test method 'verify_non_valid_parameters(param_key, params)' if it identifies the
    negative value of a given parameter and returns ValueError"""
    param_key, params = 'f_max', {'f_max': "text"}
    with pytest.raises(ValueError):
        Lowland.verify_non_valid_parameters(param_key, params)
        Highland.verify_non_valid_parameters(param_key, params)


@pytest.mark.parametrize("age, weight", [(5, 40), (10, 20), (30, 50), (20, 50)])
class TestLandscape:

    @pytest.mark.parametrize("age, weight", [(5, 40), (10, 20), (30, 50), (20, 50)])
    def create_map_for_test(self, age, weight):
        geogr = """\
                   WWW
                   WLW
                   WWW"""
        geogr = textwrap.dedent(geogr)
        ini_herbs = [
            {
                "loc": (2, 2),
                "pop": [{"species": "Herbivore", "age": age, "weight": weight}],
            }]

        seed = 123213
        t_sim = BioSim(geogr, ini_herbs, seed)
        loc = (1, 1)

        return t_sim, loc

    def test_fauna_aging(self, age, weight):
        """Test if the method 'age_increase()' correctly increases in 1 year all
            the animal_objects stored in a specific geo_object"""

        t_sim, loc = self.create_map_for_test(age, weight)
        loc_object = t_sim.map.livable_cell_calculate()[loc]
        for _ in range(len(loc_object.initial_population['Herbivore'])):
            herb_object = loc_object.initial_population['Herbivore'][_]
            herb_age_before = herb_object.age
            loc_object.age_increase()
            herb_age_after = herb_object.age
            assert herb_age_after is (herb_age_before + 1)

    def test_herbivore_feeding(self, age, weight):
        """This test method verifies different cases for the feed_herbivore():
            a.) To check if the fodder reduces when an animal eats it.
            b.) To check if the weight of the animal increases after eat.
            c.) To check if the fitness of the animal gets updated after feeding is done.
        """
        t_sim, loc = self.create_map_for_test(age, weight)
        loc_object = t_sim.map.livable_cell_calculate()[loc]
        old_fodder = loc_object.fodder
        herb_object = loc_object.initial_population['Herbivore'][0]
        old_herb_weight = herb_object.weight
        old_herb_fitness = herb_object.fitness
        loc_object.feed_herbivore()
        updated_fodder = loc_object.fodder
        updated_herb_weight = herb_object.weight
        updated_herb_fitness = herb_object.fitness

        assert old_fodder > updated_fodder
        assert old_herb_weight < updated_herb_weight
        assert old_herb_fitness != updated_herb_fitness

    def test_carnivore_feeding(self, age, weight, mocker):
        mocker.patch('random.random', return_value=0.00115)

        """This test method verifies different cases for the feed_herbivore():
            a.) To check if the fodder reduces when an animal eats it.
            b.) To check if the weight of the animal increases after eat.
            c.) To check if the fitness of the animal gets updated after feeding is done.
        """
        ini_carns = [
            {
                "loc": (2, 2),
                "pop": [
                    {"species": "Carnivore", "age": 15, "weight": 40}
                    for _ in range(40)],
            }]
        t_sim, loc = self.create_map_for_test(age, weight)
        loc_object = t_sim.map.livable_cell_calculate()[loc]
        t_sim.add_population(ini_carns)
        carn_object = loc_object.initial_population['Carnivore'][0]
        old_carn_weight = carn_object.weight
        loc_object.feed_carnivore()
        updated_carn_weight = carn_object.weight
        assert old_carn_weight < updated_carn_weight

    def test_fauna_death(self, age, weight, mocker):
        mocker.patch('random.random', return_value=0.00001)

        """This test method verifies different cases for the feed_herbivore():
            a.) To check if the fodder reduces when an animal eats it.
            b.) To check if the weight of the animal increases after eat.
            c.) To check if the fitness of the animal gets updated after feeding is done.
        """
        ini_carns = [
            {
                "loc": (2, 2),
                "pop": [
                    {"species": "Carnivore", "age": 15, "weight": 40}
                    for _ in range(40)],
            }]
        ini_herbs = [
            {
                "loc": (1, 1),
                "pop": [
                    {"species": "Herbivore", "age": 5,
                     "weight": random.randint(1, 5)}
                    for _ in range(150)
                ],
            }
        ]
        t_sim, loc = self.create_map_for_test(age, weight)
        loc_object = t_sim.map.livable_cell_calculate()[loc]
        t_sim.add_population(ini_carns)
        t_sim.add_population(ini_herbs)
        loc_object.animal_die()
        assert len(loc_object.initial_population["Carnivore"]) < 40
        assert len(loc_object.initial_population["Herbivore"]) < 151

    def test_fauna_weight_loss(self, age, weight):
        """Test if the method 'age_increase()' correctly increases in 1 year all
            the animal_objects stored in a specific geo_object

        Parameters
        ----------
        weight : object"""
        ini_herbs = [
            {
                "loc": (2, 2),
                "pop": [
                    {"species": "Herbivore", "age": 5, "weight": 40}
                    for _ in range(150)
                ],
            }
        ]
        t_sim, loc = self.create_map_for_test(age, weight)
        t_sim.add_population(ini_herbs)
        loc_object = t_sim.map.livable_cell_calculate()[loc]
        for _ in range(len(loc_object.initial_population['Herbivore'])):
            herb_object = loc_object.initial_population['Herbivore'][_]
            herb_weight_before = herb_object.weight
            loc_object.weight_decrease()
            herb_weight_after = herb_object.weight
            assert herb_weight_after < herb_weight_before


def test_fauna_count_after_birth():
    """This test that the number of animals in the cell increases after birth or not.
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
                for _ in range(150)
            ],
        }
    ]

    seed = 23423
    t_sim = BioSim(geogr, ini_herbs, seed)
    fauna_count_before = t_sim.num_animals
    loc = (1, 1)
    loc_object = t_sim.map.livable_cell_calculate()[loc]
    loc_object.add_newborn()
    assert fauna_count_before - t_sim.num_animals < 0


def test_fauna_weight_after_birth():
    """This test that the number of animals in the cell increases after birth or not.
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
                for _ in range(150)
            ],
        }
    ]

    seed = 23423
    t_sim = BioSim(geogr, ini_herbs, seed)
    loc = (1, 1)
    loc_object = t_sim.map.livable_cell_calculate()[loc]
    fauna_weight_before = 0
    for _ in range(len(loc_object.initial_population['Herbivore'])):
        herb_object = loc_object.initial_population['Herbivore'][_]
        fauna_weight_before += herb_object.weight
    loc_object.add_newborn()
    fauna_weight_after = 0
    for _ in range(len(loc_object.initial_population['Herbivore'])):
        herb_object = loc_object.initial_population['Herbivore'][_]
        fauna_weight_after += herb_object.weight

    assert fauna_weight_after < fauna_weight_before


def test_migration():
    """This tests the migration method checking if the animals have
    moved to the all 4th neighbour cells."""

    geogr = """\
                       WWWWW
                       WLLLW
                       WHLHW
                       WDDDW
                       WWWWW"""
    geogr = textwrap.dedent(geogr)
    ini_herbs = [
        {
            "loc": (3, 3),
            "pop": [{"species": "Herbivore", "age": 5, "weight": 30}
                    for _ in range(150)
                    ],
        }]

    seed = 123213
    t_sim = BioSim(geogr, ini_herbs, seed)
    loc = (1, 1)

    neighbours = t_sim.map.neighbours_dict[loc]

    print(neighbours)



