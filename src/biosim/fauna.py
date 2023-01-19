import math
import random

"""Creating fauna class with relevant parameters appropriate"""


class Fauna:
    """
    Fauna class consisting of subclasses namely for herbivores and carnivores!!
    """

    parameters = {}

    def __init__(self, age=None, weight=None):

        """
        Defining a constructor for the weight and age of the animals.
        If the weight or age is invalid


        Parameters:
        age:int
        weight:int,float
        fitness:float
        has_migrated:boolean
        """
        if age is None:
            self.age = 0
        else:
            self.age = age

        if weight is None:
            self.weight = self.weight_default()
        elif weight < 0:
            raise ValueError("Negative weight is not allowed to enter!!")
        else:
            self.weight = weight

        self.fitness = None
        self.has_migrated = False
        self.calculate_fitness()

    def calculate_fitness(self):
        def fitness_formula(sign, x, x_half, phi_x):

            return 1.0 / (1 + math.exp(sign * phi_x * (x - x_half)))

        if self.weight == 0:
            self.fitness = 0
        else:
            self.fitness = fitness_formula(1, self.age,
                                           self.parameters['a_half'],
                                           self.parameters['phi_age']) * \
                           fitness_formula(-1, self.weight, self.parameters['w_half'],
                                           self.parameters['phi_weight'])
    def weight(self):
        return self.weight()

    def weight_default(self):

        mu = math.log(self.parameters['w_birth'] ** 2 / math.sqrt(
            self.parameters['w_birth'] ** 2 + self.parameters['sigma_birth']))
        sigma = math.sqrt(
            math.log(1 + self.parameters['sigma_birth'] ** 2 / self.parameters['w_birth'] ** 2))
        return random.lognormvariate(mu, sigma)

    def age_increase(self):

        self.age += 1

    def weight_decrease(self):

        if self.weight > 0:
            self.weight = self.weight - (self.weight * self.parameters['eta'])
        self.calculate_fitness()

    def weight_decrease_on_birth(self, child):

        if self.weight >= child.weight * child.parameters['xi']:
            self.weight -= child.weight * child.parameters['xi']
            self.calculate_fitness()
            return True
        else:
            return False

    def weight_increase_on_eat(self, amount):

        self.weight += amount * self.parameters['beta']
        self.calculate_fitness()

    def birth_prob(self, animal_number):

        zeta = self.parameters['zeta']
        w_birth = self.parameters['w_birth']
        sigma_birth = self.parameters['sigma_birth']
        gamma = self.parameters['gamma']
        result = zeta * (w_birth + sigma_birth)
        if animal_number == 1:
            prob = 0

        else:
            val1 = gamma * self.fitness * (animal_number - 1)
            prob = min(1, val1)

        return random.random() < prob and self.weight >= result

    def die(self):

        if self.weight is None:
            return True

    def die_prob(self):

        if self.fitness == 0:
            return True
        else:
            return random.random() < (self.parameters['omega'] * (1 - self.fitness))

    def kill_prob(self, target_fitness):

        """This method calculates the probability if a Carnivore will kill an animal (Herbivore)
         according to the following conditions:
            Conditions:
            -----------
                -> If fitness of the carnivore <= fitness of the herbivore, then p = 0;
                -> If 0 < ('fitness of the carnivore' -  'fitness of the
                   herbivore') < 'DeltaPhiMax', then p = ('fitness of the
                   carnivore' - 'fitness of the herbivore') / 'DeltaPhiMax';
                -> Otherwise: p =   1.
                -> The random.random() is used to get a random number and
                   check if it is less than p, then a herbivore is killed or the herbivore escapes.

            Parameters:
            ----------
                target_fitness: int or float

            Returns:
            ----------
                True if herbivore is killer else False.
            """
        killer_fitness = self.fitness
        killer_target_diff_fitness = killer_fitness - target_fitness
        delta_phi_max = self.parameters['DeltaPhiMax']

        if killer_fitness <= target_fitness:
            kill_prob = 0
        elif 0 < killer_target_diff_fitness < delta_phi_max:
            kill_prob = killer_target_diff_fitness / delta_phi_max
        else:
            kill_prob = 1

        return random.random() < kill_prob

    def move_prob(self):
        """This method calculates the probability of moving to a habitable neighbour cell.
        This takes in consideration the parameter 'mu' times the animal fitness. Both species have
        the chance of migrating, once a year, to north, south, west and east.

        Formula and conditions:
        ----------
            -> If random.random() number is less than the migrating
               probability, then an animal migrates, else does not.

        Returns
        -------
            True if an animal migrates else False.
        """
        return random.random() < self.parameters['mu'] * self.fitness

    @classmethod
    def check_not_defined_params(cls, params):
        for p in params.keys():
            if p not in cls.parameters.keys():
                raise ValueError("Parameter is not defined "+str(p))

    @classmethod
    def set_parameters(cls, params):

        cls.check_not_defined_params(params)
        cls.parameters.update(params)


class Herbivore(Fauna):
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
                  'xi': xi, 'mu': mu, 'omega': omega
                  }

    def __init__(self, age=None, weight=None):
        super().__init__(age, weight)


class Carnivore(Fauna):
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
                  'xi': xi, 'mu': mu, 'DeltaPhiMax': DeltaPhiMax, 'omega': omega}

    def __init__(self, age=None, weight=None):
        super().__init__(age, weight)
