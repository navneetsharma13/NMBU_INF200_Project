import pytest
from src.biosim.fauna import Carnivore, Herbivore
import math
import random

random.seed(1223)


class TestFauna:
    @pytest.fixture()
    def create_h_params(self):
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

        self.parameters = {'eta': eta, 'F': F, 'beta': beta, 'w_birth': w_birth,
                      'sigma_birth': sigma_birth, 'phi_age': phi_age, 'phi_weight': phi_weight,
                      'a_half': a_half, 'w_half': w_half, 'gamma': gamma, 'zeta': zeta,
                      'xi': xi, 'mu': mu, 'omega': omega}
        return self.parameters


    @pytest.fixture()
    def create_c_params(self=None):
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

        self.parameters = {'eta': eta, 'F': F, 'beta': beta, 'w_birth': w_birth,
                      'sigma_birth': sigma_birth, 'phi_age': phi_age, 'phi_weight': phi_weight,
                      'a_half': a_half, 'w_half': w_half, 'gamma': gamma, 'zeta': zeta,
                      'xi': xi, 'mu': mu, 'DeltaPhiMax': DeltaPhiMax, 'omega': omega}
        return self.parameters


    @pytest.mark.parametrize('age,weight', [(10, 20), (30, 40)])
    def test_fitness_herbivore(self,age, weight, create_h_params):
        """Test if the method 'calculate_fitness()' correctly communicates to
        the method 'fit_formula()' and returns the correct fitness of the
        animal (pop_object)'"""

        self.herbivore = Herbivore(age=age, weight=weight)
        self.herbivore.calculate_fitness()
        h_params = create_h_params
        fitness = (1 / (1 + math.exp(h_params["phi_age"] * (age - h_params["a_half"])))) * \
                  (1 / (1 + math.exp(-h_params["phi_weight"] * (weight - h_params["w_half"]))))
        assert self.herbivore.fitness == fitness


    @pytest.mark.parametrize('age,weight', [(10, 20), (30, 40), (200, 200)])
    def test_fitness_carnivore(self,age, weight, create_c_params):
        """Test if the method 'calculate_fitness()' correctly communicates to
        the method 'fit_formula()' and returns the correct fitness of the
        animal (pop_object)'"""

        self.carnivore = Carnivore(age=age, weight=weight)
        self.carnivore.calculate_fitness()
        c_params = create_c_params
        fitness = (1 / (1 + math.exp(c_params["phi_age"] * (age - c_params["a_half"])))) * \
                  (1 / (1 + math.exp(-c_params["phi_weight"] * (weight - c_params["w_half"]))))
        assert self.carnivore.fitness == fitness


    def test_animal(self):
        """"""
        self.h = Herbivore()
        self.c = Carnivore()
        for _ in range(100):
            assert self.h.age == 0
            assert self.c.age == 0


    @pytest.mark.parametrize('weight', [10, 20])
    def test_herbivore_non_negative_weight(self,weight):
        """
        test if animal age is  non-negative
        """
        self.h = Herbivore(weight=weight)
        # c = Carnivore(weight=weight)
        assert self.h.weight >= 0
        # assert c.weight >= 0


    @pytest.mark.parametrize('weight', [10, 20])
    def test_carnivore_non_negative_weight(self,weight):
        """
        test if animal age is  non-negative
        """
        self.c = Carnivore(weight=weight)
        # c = Carnivore(weight=weight)
        assert self.c.weight >= 0
        # assert c.weight >= 0


    #
    @pytest.mark.parametrize("age,weight", [(10, 20), (0, 10), (100, 80)])
    def test_herbivore_aging(self,age, weight):
        """
        test every year animal age updates
        """
        self.herb = Herbivore(age, weight)
        n = 100
        for _ in range(n):
            self.herb.age_increase()
        assert self.herb.age == age + n


    @pytest.mark.parametrize("age,weight", [(10, 20), (0, 10), (100, 80)])
    def test_carnivore_aging(self,age, weight):
        """
        test every year animal age updates
        """
        self.carn = Carnivore(age, weight)
        n = 100
        for _ in range(n):
            self.carn.age_increase()
        assert self.carn.age == age + n


    #
    @pytest.mark.parametrize('weight', [0, 10, 20, 30, 40, 60, 70])
    def test_herbivore_weight_loss(self,weight, create_h_params):
        """
        Test if animal looses weight
        """
        self.h_params = create_h_params
        self.herb = Herbivore(weight=weight)

        for _ in range(5):
            weight = weight - self.h_params['eta'] * weight
            self.herb.weight_decrease()

        assert self.herb.weight == weight


    @pytest.mark.parametrize('weight', [0, 10, 20, 30, 40, 60, 70])
    def test_carnivore_weight_loss(self,weight, create_c_params):
        """
        Test if animal looses weight
        """
        self.c_params = create_c_params
        self.carn = Carnivore(weight=weight)

        for _ in range(5):
            weight = weight - self.c_params['eta'] * weight
            self.carn.weight_decrease()

        assert self.carn.weight == weight


    #
    @pytest.mark.parametrize("age,weight", [(10, 20), (0, 0), (100, 80), (200, 200)])
    def test_fitness_range(self,age, weight):
        """
        test fitness value is between 0 and 1
        """
        self.herb = Herbivore(age, weight)
        self.carn = Carnivore(age, weight)
        assert 1 >= self.herb.fitness >= 0
        assert 1 >= self.carn.fitness >= 0


    #
    @pytest.mark.parametrize("age,weight", [(10, 20), (100, 80), (200, 200)])
    def test_fitness_update_herb(self,age, weight, create_h_params):
        """
        test fitness is updated when weight is changed
        """
        self.h_params = create_h_params
        self.herb = Herbivore(age, weight)
        self.herb.weight_decrease()

        weight = weight - self.h_params['eta'] * weight

        fitness = (1 / (1 + math.exp(self.h_params["phi_age"] * (age - self.h_params["a_half"])))) * \
                  (1 / (1 + math.exp(-self.h_params["phi_weight"] * (weight - self.h_params["w_half"]))))

        if weight == 0:
            fitness = 0

        assert self.herb.fitness == fitness


    @pytest.mark.parametrize("age,weight", [(10, 20), (100, 80), (200, 200)])
    def test_fitness_update_carn(self,age, weight, create_c_params):
        """
        test fitness is updated when weight is changed
        """
        self.c_params = create_c_params
        self.carn = Carnivore(age, weight)
        self.carn.weight_decrease()

        weight = weight - self.c_params['eta'] * weight

        fitness = (1 / (1 + math.exp(self.c_params["phi_age"] * (age - self.c_params["a_half"])))) * \
                  (1 / (1 + math.exp(-self.c_params["phi_weight"] * (weight - self.c_params["w_half"]))))

        if weight == 0:
            fitness = 0

        assert self.carn.fitness == fitness


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
    @pytest.mark.parametrize("species_count", [2, 3, 4])
    @pytest.mark.parametrize("age,weight, status", [(10, 34, True), (0, 40, True), (10, 50, True)])
    def test_herbivore_birth_probability_success(self,age, weight, status, mocker, species_count):
        mocker.patch('random.random', return_value=0.01)

        self.herb = Herbivore(age, weight)
        assert self.herb.birth_prob(species_count) == status


    @pytest.mark.parametrize("species_count", [2, 3, 4])
    @pytest.mark.parametrize("age,weight, status", [(10, 34, True), (0, 40, True), (10, 50, True)])
    def test_carnivore_birth_probability_success(self,age, weight, status, mocker, species_count):
        mocker.patch('random.random', return_value=0.01)

        self.carn = Carnivore(age, weight)
        assert self.carn.birth_prob(species_count) == status


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
    @pytest.mark.parametrize("age,weight, status",
                             [(10, 20, False), (100, 80, False), (200, 200, False)])
    def test_animal_certain_survival(self,age, weight, status, mocker):
        mocker.patch('random.random', return_value=0.8)

        self.herb = Herbivore(age, weight)
        self.carn = Carnivore(age, weight)
        assert self.herb.die_prob() == status
        assert self.carn.die_prob() == status


    @pytest.mark.parametrize("age,weight, status", [(10, 20, True), (100, 80, True),
                                                    (200, 200, True), (0, 0, True)])
    def test_animal_certain_death(self, age, weight, status, mocker):
        mocker.patch('random.random', return_value=0.00001)

        self.herb = Herbivore(age, weight)
        self.carn = Carnivore(age, weight)
        assert self.herb.die_prob() == status
        assert self.carn.die_prob() == status
    #
#
