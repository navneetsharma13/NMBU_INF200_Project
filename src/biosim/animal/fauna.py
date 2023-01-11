import math
import random

"""Creating fauna class with relevant parameters appropriate"""


class Fauna:
    """
    Fauna class consisting of subclasses namely for herbivores and carnivores!!
    """
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
        else:
            # self.raise_type_error(weight)
            self.weight = weight

        self.fitness = None
        self.calculate_fitness(self.age,self.weight,self.parameters)

    def raise_type_error(val):
        if isinstance(val, (int, float)) is False:
            raise ValueError(str(val) + "cannot be a value type,it has to be int or float")

    def weight(self):
        return self.weight()

    def weight_default(cls):
        mu = math.log(cls.parameters['w_birth'] ** 2 / math.sqrt(
            cls.parameters['w_birth'] ** 2 + cls.parameters['sigma_birth']))
        sigma = math.log(1 + cls.parameters['sigma_birth'] ** 2 / cls.parameters['w_birth'] ** 2)
        return random.lognormvariate(mu, sigma)

    def age_increase(self):
        self.age += 1

    def weight_decrease(self):
        self._weight = self.weight - (self.weight * self.parameters['eta'])
        self.fitness = self.calculate_fitness(self.age,self.weight,self.parameters)



    def calculate_fitness(cls,age,weight,parameters):
        def fitness_formula(sign, x, x_half, phi_x):

            return 1.0/(1 + math.exp(sign * phi_x * (x - x_half)))

        if weight == 0:
            phi = 0
        else:
            phi = fitness_formula(1,age,parameters['a_half'],parameters['phi_age'])* fitness_formula(-1,weight,parameters['w_half'],parameters['phi_weight'])
            # cls.check_phi_borders(phi)
            return phi

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
        if self.weight >= zeta * (w_birth + sigma_birth):
            return random.random() < min(1, gamma *
                                         self.fitness * (animal_number))
        else:
            return False

    def weight_decrease_on_birth(self, child):
        if self.weight >= child.weight * child.parameters['xi']:
            self._weight -= child.weight * child.parameters['xi']

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
