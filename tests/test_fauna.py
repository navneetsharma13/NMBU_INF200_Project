from typing import Dict, Any

import pytest
from src.biosim.fauna import Carnivore, Herbivore
from math import isclose
import math
import numpy as np
import random

random.seed(1223)

@pytest.fixture()
def create_h_params():

    eta = 0.05
    F = 10.0
    beta = 0.9
    w_birth = 8.0
    sigma_birth = 1.5
    phi_age = 0.6
    phi_weight = 0.1
    a_half = 40
    w_half = 10.0
    gamma = 0.2
    zeta = 3.5
    xi = 1.2
    mu = 0.25
    omega = 0.4

    parameters = {'eta': eta, 'F': F, 'beta': beta, 'w_birth': w_birth,
                  'sigma_birth': sigma_birth, 'phi_age': phi_age, 'phi_weight': phi_weight,
                  'a_half': a_half, 'w_half': w_half, 'gamma': gamma, 'zeta': zeta,
                  'xi': xi, 'mu': mu, 'omega': omega}
    return parameters

@pytest.fixture()
def create_c_params():

    eta = 0.125
    F = 50.0
    beta = 0.75
    w_birth = 6.0
    sigma_birth = 1.0
    phi_age = 0.3
    phi_weight = 0.4
    a_half = 40
    w_half = 4.0
    gamma = 0.8
    zeta = 3.5
    xi = 1.1
    mu = 0.4
    DeltaPhiMax = 10.0
    omega = 0.8

    parameters = {'eta': eta, 'F': F, 'beta': beta, 'w_birth': w_birth,
                  'sigma_birth': sigma_birth, 'phi_age': phi_age, 'phi_weight': phi_weight,
                  'a_half': a_half, 'w_half': w_half, 'gamma': gamma, 'zeta': zeta,
                  'xi': xi, 'mu': mu, 'DeltaPhiMax': DeltaPhiMax,'omega': omega}
    return parameters

@pytest.mark.parametrize('age,weight', [(10, 20),(30,40)])
def test_fitness_herbivore(age, weight, create_h_params):
    """Test if the method 'calculate_fitness()' correctly communicates to
    the method 'fit_formula()' and returns the correct fitness of the
    animal (pop_object)'"""

    herbivore = Herbivore(age=age, weight=weight)
    herbivore.calculate_fitness()
    h_params = create_h_params
    fitness = (1 / (1 + math.exp(h_params["phi_age"] * (age - h_params["a_half"])))) * \
              (1 / (1 + math.exp(-h_params["phi_weight"] * (weight - h_params["w_half"]))))
    assert herbivore.fitness == fitness

@pytest.mark.parametrize('age,weight', [(10, 20),(30,40),(200,200)])
def test_fitness_carnivore(age, weight, create_c_params):
    """Test if the method 'calculate_fitness()' correctly communicates to
    the method 'fit_formula()' and returns the correct fitness of the
    animal (pop_object)'"""

    carnivore = Carnivore(age=age, weight=weight)
    carnivore.calculate_fitness()
    c_params = create_c_params
    fitness = (1 / (1 + math.exp(c_params["phi_age"] * (age - c_params["a_half"])))) * \
              (1 / (1 + math.exp(-c_params["phi_weight"] * (weight - c_params["w_half"]))))
    assert carnivore.fitness == fitness



def test_animal():
    """"""
    h = Herbivore()
    c = Carnivore()
    for _ in range(100):
        assert h.age == 0
        assert c.age == 0


@pytest.mark.parametrize('weight', [10, 20])
def test_herbivore_non_negative_weight(weight):
    """
    test if animal age is  non-negative
    """
    h = Herbivore(weight=weight)
    # c = Carnivore(weight=weight)
    assert h.weight >= 0
    # assert c.weight >= 0
@pytest.mark.parametrize('weight', [10, 20])
def test_carnivore_non_negative_weight(weight):
    """
    test if animal age is  non-negative
    """
    c = Carnivore(weight=weight)
    # c = Carnivore(weight=weight)
    assert c.weight >= 0
    # assert c.weight >= 0

#
@pytest.mark.parametrize("age,weight",[(10,20),(0,10),(100,80)])
def test_herbivore_aging(age, weight):
    """
    test every year animal age updates
    """
    herb = Herbivore(age,weight)
    n = 100
    for _ in range(n):
        herb.age_increase()
    assert herb.age == age + n

@pytest.mark.parametrize("age,weight",[(10,20),(0,10),(100,80)])
def test_carnivore_aging(age, weight):
    """
    test every year animal age updates
    """
    carn = Carnivore(age,weight)
    n = 100
    for _ in range(n):
        carn.age_increase()
    assert carn.age == age + n
#
@pytest.mark.parametrize('weight', [0, 10, 20, 30, 40, 60, 70])
def test_herbivore_weight_loss(weight, create_h_params):
    """
    Test if animal looses weight
    """
    h_params = create_h_params
    herb = Herbivore(weight=weight)


    for _ in range(5):
        weight = weight - h_params['eta'] * weight
        herb.weight_decrease()

    assert herb.weight == weight

@pytest.mark.parametrize('weight', [0, 10, 20, 30, 40, 60, 70])
def test_carnivore_weight_loss(weight, create_c_params):
    """
    Test if animal looses weight
    """
    c_params = create_c_params
    carn = Carnivore(weight=weight)


    for _ in range(5):
        weight = weight - c_params['eta'] * weight
        carn.weight_decrease()

    assert carn.weight == weight

#
@pytest.mark.parametrize("age,weight",[(10,20),(0,0),(100,80), (200,200)])
def test_fitness_range(age, weight):
    """
    test fitness value is between 0 and 1
    """
    herb = Herbivore(age, weight)
    carn = Carnivore(age,weight)
    assert 1 >= herb.fitness >= 0
    assert 1 >= carn.fitness >= 0

#
@pytest.mark.parametrize("age,weight",[(10,20),(100,80), (200,200)])
def test_fitness_update_herb(age, weight, create_h_params):
    """
    test fitness is updated when weight is changed
    """
    h_params = create_h_params
    herb = Herbivore(age, weight)
    herb.weight_decrease()

    weight = weight - h_params['eta'] * weight

    fitness = (1 / (1 + math.exp(h_params["phi_age"] * (age - h_params["a_half"])))) * \
              (1 / (1 + math.exp(-h_params["phi_weight"] * (weight - h_params["w_half"]))))

    if weight == 0:
        fitness = 0

    assert herb.fitness == fitness

@pytest.mark.parametrize("age,weight",[(10,20),(100,80), (200,200)])
def test_fitness_update_carn(age, weight, create_c_params):
    """
    test fitness is updated when weight is changed
    """
    c_params = create_c_params
    carn = Carnivore(age, weight)
    carn.weight_decrease()

    weight = weight - c_params['eta'] * weight

    fitness = (1 / (1 + math.exp(c_params["phi_age"] * (age - c_params["a_half"])))) * \
              (1 / (1 + math.exp(-c_params["phi_weight"] * (weight - c_params["w_half"]))))

    if weight == 0:
        fitness = 0

    assert carn.fitness == fitness
#
# def test_animal_death():
#     """
#     test that animal dies when fitness is 0 or with
#     certain probability omega(1 - fitness)
#     """
#     herb = Herbivore(10, 50)
#     herb.fitness = 0
#
#     for _ in range(100):
#         assert herb.die_prob() is True
#
#
@pytest.mark.parametrize("species_count",[2,3,4])
@pytest.mark.parametrize("age,weight, status",[(10,34,True),(0,40,True),(10,50,True)])
def test_herbivore_birth_probability_success(age,weight,status,mocker, species_count):
    mocker.patch('random.random',return_value=0.01)

    herb = Herbivore(age, weight)
    assert herb.birth_prob(species_count)==status

@pytest.mark.parametrize("species_count",[2,3,4])
@pytest.mark.parametrize("age,weight, status",[(10,34,True),(0,40,True),(10,50,True)])
def test_carnivore_birth_probability_success(age,weight,status,mocker, species_count):
    mocker.patch('random.random',return_value=0.01)

    carn = Carnivore(age, weight)
    assert carn.birth_prob(species_count)==status
#
#
# def test_update_weight_after_birth():
#     """
#     test that the weight of the mother is
#     reduced by xi times the weight of the
#     baby after reproduction
#     """
#     herb = Herbivore(20, 40)
#     weight_before_birth = herb.weight
#     baby = Herbivore(weight=10)
#     herb.weight_decrease_on_birth(baby)
#     assert herb.weight < weight_before_birth
#
@pytest.mark.parametrize("age,weight, status",[(10,20, False),(100,80, False), (200,200, False)])
def test_animal_certain_survival(age, weight, status, mocker):
    mocker.patch('random.random', return_value=0.8)

    herb=Herbivore(age,weight)
    carn=Carnivore(age,weight)
    assert herb.die_prob() == status
    assert carn.die_prob() == status

@pytest.mark.parametrize("age,weight, status",[(10,20, True),(100,80, True),
                                               (200,200, True), (0,0, True)])
def test_animal_certain_death(age, weight, status, mocker):
    mocker.patch('random.random', return_value=0.00001)

    herb=Herbivore(age,weight)
    carn=Carnivore(age,weight)
    assert herb.die_prob() == status
    assert carn.die_prob() == status
#
#
