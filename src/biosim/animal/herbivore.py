from fauna import *

class Herbivore(Fauna):

    eta=0.05
    F=10.0
    beta=0.9
    w_birth=8.0
    sigma_birth=1.5
    phi_age=0.2
    phi_weight=0.1
    a_half=40
    w_half=10.0
    gamma=0.8
    zeta=3.5
    xi=1.2
    mu=0.25
    lambda_=1.0
    omega=0.4

    parameters = {'eta':eta, 'F': F, 'beta': beta, 'w_birth': w_birth,
                  'sigma_birth': sigma_birth, 'phi_age': phi_age, 'phi_weight': phi_weight,
                  'a_half': a_half, 'w_half': w_half, 'gamma': gamma, 'zeta': zeta,
                  'xi': xi, 'mu': mu, 'lambda': lambda_, 'omega': omega
                  }

    def __init__(self, age=None, weight=None):
        super().__init__(weight, age)
