"""
This is the geography pytest package which is a test package for the  BioSim packages written for
 the INF200 project January 2022.
"""

__author__ = "Navneet Sharma and Sushant Kumar Srivastava"
__email__ = "navneet.sharma@nmbu.no and sushant.kumar.sirvastava@nmbu.no"

import random
import textwrap

import pytest
import random as rd
import numpy as np
from src.biosim.landscape import Lowland, Highland
from src.biosim.simulation import BioSim


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


@pytest.mark.parametrize("age, weight", [(10, 20), (100, 80), (200, 200)])
def create_map_for_test(age, weight):
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


@pytest.mark.parametrize("age, weight", [(10, 20), (100, 80), (200, 200)])
def test_fauna_aging(age, weight):
    """Test if the method 'age_increase()' correctly increases in 1 year all
        the animal_objects stored in a specific geo_object"""

    t_sim, loc = create_map_for_test(age, weight)
    loc_object = t_sim.map.livable_cell_calculate()[loc]
    for _ in range(len(loc_object.initial_population['Herbivore'])):
        herb_object = loc_object.initial_population['Herbivore'][_]
        herb_age_before = herb_object.age
        loc_object.age_increase()
        herb_age_after = herb_object.age
        assert herb_age_after is (herb_age_before + 1)


@pytest.mark.parametrize("age, weight", [(10, 20), (100, 80), (200, 200)])
def test_herbivore_feeding(age, weight):
    """This test method verifies different cases for the feed_herbivore():
        a.) To check if the fodder reduces when an animal eats it.
        b.) To check if the weight of the animal increases after eat.
        c.) To check if the fitness of the animal gets updated after feeding is done.
    """
    t_sim, loc = create_map_for_test(age, weight)
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



