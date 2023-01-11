from fauna import Fauna

class Carnivore(Fauna):

    eta=0.125
    F=50.0
    beta=0.75
    w_birth=6.0
    sigma_birth=1.0
    phi_age=0.4
    phi_weight=0.4
    a_half=60
    w_half=4.0
    gamma=0.8
    zeta=3.5
    xi=1.1
    mu=0.4
    DeltaPhiMax=10.0
    lambda_=1.0
    omega=0.9

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
    #     if self._fitness <= target_herbivore.fitness:
    #         self._carnivore_consume_herbivore_prob=0
    #
    #     elif 0 < self._fitness-target_herbivore.fitness < self.parameters['DeltaPhiMaX']: