import math
import random

"""Creating fauna class with relevant parameters appropriate"""


class Fauna:
    """
    Fauna class consisting of subclasses namely for herbivores and carnivores!!
    """
    fitness = 0
    parameters = {}

    def __init__(self, weight=None, age=None):

        """
        Defining a constructor for the weight and age of the animals.
        If the weight or age is invalid


        Parameters:
        age:int
        weight:int,float
        """
        if age is None:
            self.age = 0
        else:
            # self.raise_type_error(age)
            self.age = age

        if weight is None:
            self.weight = self.weight_default()
        elif weight<0:
            raise ValueError("Negative weight is not allowed to enter!!")
        else:
            # self.raise_type_error(weight)
            self.weight = weight

        self.fitness = self.calculate_fitness(self.age, self.weight, self.parameters)

    # def raise_type_error(val):
    #     if isinstance(val, (int, float)) is False:
    #         raise ValueError(str(val) + "cannot be a value type,it has to be int or float")

    def weight(self):
        return self.weight()

    @classmethod
    def weight_default(cls):
        mu = math.log(cls.parameters['w_birth'] ** 2 / math.sqrt(
            cls.parameters['w_birth'] ** 2 + cls.parameters['sigma_birth']))
        sigma = math.log(1 + cls.parameters['sigma_birth'] ** 2 / cls.parameters['w_birth'] ** 2)
        return random.lognormvariate(mu, sigma)

    def age_increase(self):
        self.age += 1

    def weight_decrease(self):
        if self.weight>0:
            self.weight = self.weight - (self.weight * self.parameters['eta'])
        self.fitness = self.calculate_fitness(self.age, self.weight, self.parameters)

    @classmethod
    def calculate_fitness(cls, age, weight, parameters):
        def fitness_formula(sign, x, x_half, phi_x):

            return 1.0 / (1 + math.exp(sign * phi_x * (x - x_half)))

        if weight == 0:
            fitness = 0
        else:
            fitness = fitness_formula(1, age, parameters['a_half'],
                                      parameters['phi_age']) * fitness_formula(-1, weight,
                                                                               parameters['w_half'],
                                                                               parameters[
                                                                                   'phi_weight'])
            # cls.check_phi_borders(fitness)
        return fitness

    @classmethod
    # def check_phi_borders(cls,phi):
    #     if phi>1 or phi<0:
    #         raise ValueError("The Parameter 'phi' calculated is not in border 0,1")
    # def migrate_prob(self):
    #
    #     migrate_prob = self.parameters['mu'] * self.fitness
    #     if migrate_prob > random.random():
    #         return True
    def birth_prob(self, animal_number):
        zeta = self.parameters['zeta']
        w_birth = self.parameters['w_birth']
        sigma_birth = self.parameters['sigma_birth']
        gamma = self.parameters['gamma']
        result=zeta*(w_birth+sigma_birth)
        prob=0
        if animal_number==1:
            prob=0

        else:
            p = min(1,gamma*self.fitness*(animal_number-1))

        return random.random() < prob and self.weight()> result

    def weight_decrease_on_birth(self, child):
        if self.weight >= child.weight * child.parameters['xi']:
            self.weight -= child.weight * child.parameters['xi']

    def die(self):
        if self.weight is None:
            return True

    def die_prob(self):

        if self.fitness == 0:
            return True
        else:
            return random.random() < (self.parameters['omega'] * (1 - self.fitness))

    def weight_increase_on_eat(self, amount):

        self.weight += amount * self.parameters['beta']


class Herbivore(Fauna):
    eta = 0.05
    F = 10.0
    beta = 0.9
    w_birth = 8.0
    sigma_birth = 1.5
    phi_age = 0.2
    phi_weight = 0.1
    a_half = 40
    w_half = 10.0
    gamma = 0.8
    zeta = 3.5
    xi = 1.2
    mu = 0.25
    lambda_ = 1.0
    omega = 0.4

    parameters = {'eta': eta, 'F': F, 'beta': beta, 'w_birth': w_birth,
                  'sigma_birth': sigma_birth, 'phi_age': phi_age, 'phi_weight': phi_weight,
                  'a_half': a_half, 'w_half': w_half, 'gamma': gamma, 'zeta': zeta,
                  'xi': xi, 'mu': mu, 'lambda': lambda_, 'omega': omega
                  }

    def __init__(self, age=None, weight=None):
        super().__init__(weight, age)


class Carnivore(Fauna):
    eta = 0.125
    F = 50.0
    beta = 0.75
    w_birth = 6.0
    sigma_birth = 1.0
    phi_age = 0.4
    phi_weight = 0.4
    a_half = 60
    w_half = 4.0
    gamma = 0.8
    zeta = 3.5
    xi = 1.1
    mu = 0.4
    DeltaPhiMax = 10.0
    lambda_ = 1.0
    omega = 0.9

    parameters = {'eta': eta, 'F': F, 'beta': beta, 'w_birth': w_birth,
                  'sigma_birth': sigma_birth, 'phi_age': phi_age, 'phi_weight': phi_weight,
                  'a_half': a_half, 'w_half': w_half, 'gamma': gamma, 'zeta': zeta,
                  'xi': xi, 'mu': mu, 'DeltaPhiMax': DeltaPhiMax, 'lambda': lambda_,
                  'omega': omega}

    def __init__(self, age=None, weight=None):
        super().__init__(weight, age)
        self._carnivore_consume_herbivore_prob = None

    # def carnivore_consume_herbivore_prob(self,target_herbivore):
    #
    #     if self.fitness <= target_herbivore.fitness:
    #         self._carnivore_consume_herbivore_prob=0
    #
    #     elif 0 < self.fitness-target_herbivore.fitness < self.parameters['DeltaPhiMaX']:
