import pytest
from src.biosim.fauna import Carnivore, Herbivore
from math import isclose
import numpy as np
import random


random.seed(1223)

@pytest.mark.parametrize('age,weight',[(10,20)])
def test_fitness(age,weight):
    """Test if the method 'calculate_fitness()' correctly communicates to
    the method 'fit_formula()' and returns the correct fitness of the
    animal (pop_object)'"""

    herbivore = Herbivore(age=age,weight=weight)
    assert isclose(herbivore.calculate_fitness(herbivore.age,
                                                herbivore.weight,
                                                herbivore.parameters),
                    0.7292,abs_tol=10**-2)
    # assert ((carnivore.calculate_fitness(carnivore.age,
    #                                      carnivore.weight,
    #                                      carnivore.parameters),
    #          0.999969))




def test_animal():
    """"""
    h = Herbivore()
    for _ in range(100):
        assert h.age == 0


def test_herbivore_parameters():
    """ Tests that the given parameters are in the list of herbivor
    parameters"""
    keys_list = ['w_birth', 'sigma_birth', 'beta', 'eta', 'a_half',
                 'phi_age', 'w_half', 'phi_weight', 'mu', 'lambda',
                 'gamma', 'zeta', 'xi', 'omega', 'F', 'DeltaPhiMax',]
    h = Herbivore()
    assert [key in h.parameters for key in keys_list]

@pytest.mark.parametrize('weight',[10,20])
def test_herbivore_non_negative_weight(weight):
    """
    test if animal age is  non-negative
    """
    h = Herbivore(weight=weight)
    # c = Carnivore(weight=weight)
    assert h.weight >= 0
    # assert c.weight >= 0


def test_herbivore_aging():
    """
    test every year animal age updates
    """
    herb = Herbivore(10, 50)
    before_age = herb.age
    len=100
    for _ in range(len):
        herb.age_increase()
    assert herb.age == before_age + len

@pytest.mark.parametrize('weight',[10,20,30,40,60,70])
def test_herbivore_weight_loss(weight):
    """
    Test if animal looses weight
    """
    herb = Herbivore(weight=weight)
    before_weight = herb.weight
    for _ in range(20):
        herb.weight_decrease()
    assert before_weight > herb.weight


def test_fitness_range():
    """
    test fitness value is between 0 and 1
    """
    herb = Herbivore(random.randrange(0, 100), random.randrange(0, 100))
    # carn = Carnivore(random.randrange(0, 100), random.randrange(0, 100))
    assert 1 >= herb.fitness >= 0
    # assert 1 >= carn.fitness >= 0


def test_fitness_update():
    """
    test fitness is updated when weight is changed
    """
    herb = Herbivore(10, 50)
    before_fitness = herb.fitness
    herb.weight_decrease()
    assert herb.fitness != before_fitness


def test_animal_death():
    """
    test that animal dies when fitness is 0 or with
    certain probability omega(1 - fitness)
    """
    herb = Herbivore(10, 50)
    herb.fitness = 0

    for _ in range(100):
        assert herb.die_prob() is True


def test_herbivore_birth_probability():
    """
    1. Test no birth if single herbivore or carnivore
    2. Test no birth if weight of herbivore or
    carnivore is less than output of following
    condition:
        xi(w_birth + sigma_birth)
    """
    herb = Herbivore(20, 50)
    assert not herb.birth_prob(3)

    # animal = Carnivore(10, 50)
    herb.weight = 5
    assert not herb.birth_prob(200)


def test_update_weight_after_birth():
    """
    test that the weight of the mother is
    reduced by xi times the weight of the
    baby after reproduction
    """
    herb = Herbivore(20, 40)
    weight_before_birth = herb.weight
    baby = Herbivore(weight=10)
    herb.weight_decrease_on_birth(baby)
    assert herb.weight < weight_before_birth
