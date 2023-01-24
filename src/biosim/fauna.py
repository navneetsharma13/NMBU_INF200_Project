
"""
This is the Fauna model which functions with the Biosim package written for
the INF200 project January 2023.
"""

__author__ = "Navneet Sharma and Sushant Kumar Srivastava"
__email__ = "navneet.sharma@nmbu.no and sushant.kumar.srivastava@nmbu.no"

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
        ------------
        age : int
        weight : int,float
        fitness : float
        has_migrated : boolean
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
        """This method calculates and returns the overall physical condition (fitness) of an animal
         which is based on age and weight using the function fitness_formula:

        Formula and conditions:
        ------------------------
            phi = if 'omega' <= 0: 0
                  else: fit_formula('age', 'age_1/2', 'phi_age') X
                     fit_formula(-'weight', 'weight_1/2', 'phi_weight')
        """

        def fitness_formula(sign, x, x_half, phi_x):
            """This method returns the fitness formula used to calculate the physical condition
            (fitness) of an animal (pop_object).

            Formula and conditions:
            -------------------------
            1.0 / (1 + \\e^{\\pm * \\phi * (x - x_{1/2} )})

            Parameters:
            -------------
                sign: int or float
                    The sign with identifies age (+) or weight (-);

                x:  int or float
                    This is age or weight;

                x_half: int or float
                   This is the parameter 'age_half' or 'weight_half';

                phi_x: int or float
                    This is the parameter 'phi_age' or 'phi_weight'.

            Returns:
            ----------
                The fitness formula calculated in float type.
            """

            return 1.0 / (1 + math.exp(sign * phi_x * (x - x_half)))

        if self.weight == 0:
            self.fitness = 0
        else:
            self.fitness = fitness_formula(1, self.age,
                                           self.parameters['a_half'],
                                           self.parameters['phi_age']) * \
                           fitness_formula(-1, self.weight, self.parameters['w_half'],
                                           self.parameters['phi_weight'])

    def weight_default(self):
        """This method calculates the default weight of the animal based on lognormvariate by
        taking in the parameters such as mu and sigma.

        Formula and conditions:
        -----------------------
            mu=log(w_birth**2/sqrt(w_birth**2+sigma+birth)
            sigma=sqrt(log(1+sigma_birth**2/w_birth**2)

        Returns:
        ----------
            The weight of the animal calculated by taking lognormvariate(mu,sigma).

        """
        mu = math.log(self.parameters['w_birth'] ** 2 / math.sqrt(
            self.parameters['w_birth'] ** 2 + self.parameters['sigma_birth']))
        sigma = math.sqrt(
            math.log(1 + self.parameters['sigma_birth'] ** 2 / self.parameters['w_birth'] ** 2))
        return random.lognormvariate(mu, sigma)

    def age_increase(self):
        """This function increases the animal age by one"""
        self.age += 1

    def weight_decrease(self):
        """This method decreases the weight of the animal, in yearly basis, according to the
         weight_loss_rate.

        Formula and conditions:
        ------------------------
            weight_loss_rate: 'eta' * 'weight';
            yearly_weight_loss: 'weight' - 'weight_loss_rate';

            After the weight is decreased, the fitness of the animal is updated by the method
            'calculate_fitness()'.
        """

        if self.weight > 0:
            self.weight = self.weight - (self.weight * self.parameters['eta'])
        self.calculate_fitness()

    def weight_decrease_on_birth(self, child):
        """This method, when called, updates the weight of the animal
        after giving birth, according to the formula: 'xi' * the child
        weight. Then it updates the fitness.

        Parameters:
        ------------
            if weight is decreased: True
            if weight  is not decreased: False
        """

        if self.weight >= child.weight * child.parameters['xi']:
            self.weight -= child.weight * child.parameters['xi']
            self.calculate_fitness()
            return True
        else:
            return False

    def weight_increase_on_eat(self, amount):
        """This method increases the weight of the animal, in yearly
        basis, by the amount eaten times 'beta',after which the
        fitness of the animal is calculated.

        Parameters:
        ------------
            amount_eaten: int or float
        """

        self.weight += amount * self.parameters['beta']
        self.calculate_fitness()

    def birth_prob(self, animal_number):
        """This method calculates the probability of giving birth
        for an animal according to the following conditions:

        Formula and conditions:
        -------------------------
            If the number of animals of a species is 1, then the
            probability is 0;
            If the weight of the animal is less than 'zeta' * ('w_birth' + 'sigma_birth')
            ,then the probability is 0;
            Else, the probability is the minimum between 1 or
            'gamma' * the animal fitness * (number of animals of
            the specie - 1);
            random.random() is used to get a random number and
            check if is less than the probability of birth, then,
            if True, there is a offspring, else there is not.

        Parameters:
        -------------
            number_specie_objects: int or float

        Returns:
        ----------
            True if the animal gives birth else False.
        """

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
        """This method calculates whether an animal will die if its weight is zero.

        Returns:
        ----------
            True if the animal dies else False.
        """

        if self.weight is None:
            return True

    def die_prob(self):
        """An animal dies with the following conditions.

        Formula and conditions:
        -------------------------
            If its fitness is 0, or With probability if 'omega' * (1 - animal_fitness).
            If np.random.random() number is less than the die probability, then an animal dies,
            else does not.

        Returns
        ----------
            True if the animal dies else False.
         """
        if self.fitness == 0:
            return True
        else:
            return random.random() < (self.parameters['omega'] * (1 - self.fitness))

    def kill_prob(self, target_fitness):

        """This method calculates the probability if a Carnivore will kill an animal (Herbivore)
         according to the following conditions:
        Conditions:
        -----------
            If fitness of the carnivore <= fitness of the herbivore, then p = 0;
            If 0 < ('fitness of the carnivore' -  'fitness of the herbivore') < 'DeltaPhiMax', then
            p = ('fitness of the carnivore' - 'fitness of the herbivore') / 'DeltaPhiMax';
            Otherwise: p =   1.
            The random.random() is used to get a random number and check if it is less than p, then
            a herbivore is killed or the herbivore escapes.

        Parameters:
        ------------
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
        -------------------------
            If random.random() number is less than the migrating probability, then an animal
             migrates, else does not.

        Returns
        ---------
            True if an animal migrates else False.
        """
        return random.random() < self.parameters['mu'] * self.fitness

    @classmethod
    def check_not_defined_params(cls, params):
        """This method checks undefined parameters and raises a ValueError
        if necessary.

        Parameters:
        -------------
            params: dict
        """
        for p in params.keys():
            if p not in cls.parameters.keys():
                raise ValueError("Parameter is not defined " + str(p))

    @classmethod
    def set_parameters(cls, params):
        """This method sets the parameters for the animals.

        Parameters:
        -------------
            params: dict
        """
        cls.check_not_defined_params(params)
        cls.parameters.update(params)


class Herbivore(Fauna):
    """The herbivores find fodder in Highland and Lowland, although they can reside in desert also
    they move with equal probability in all 4 directions.
    """
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
        """Constructor for Herbivore class.
        """
        super().__init__(age, weight)


class Carnivore(Fauna):
    """The carnivores prey on herbivores in lowland, highland and desert.
    """
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
        """Constructor for Carnivore class.
        """
        super().__init__(age, weight)
