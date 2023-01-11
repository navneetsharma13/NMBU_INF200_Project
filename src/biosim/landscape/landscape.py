"""
Landscape Class and subclasses (Lowland, Highland, Desert and Water).
Landscape class is a parent class, all objects are instantiated from the
Lowland, Highland, Desert and Water subclasses
"""

from ..animal import carnivore, herbivore


class Landscape:
    parameters = {}

    def __init__(self):
        """Constructor for the landscape cells."""
        self.initial_population = {'Herbivore': [], 'Carnivore': []}
        self.population_to_add = {'Herbivore': [], 'Carnivore': []}
        self.fodder = 0

    @classmethod
    def verify_parameters(cls, params):
        """This method verifies for any wrong parameters
        passed by the user and raises a
        ValueError, if required.

        Parameters:
        ----------
            params: list
                List with the landscape's parameters.
        """
        for parameter in params.keys():
            if parameter not in cls.parameters.keys():
                raise ValueError("Wrong parameter provided: "
                                 "*{}*".format(parameter))

    @classmethod
    def verify_non_valid_parameters(cls, param_key, params):
        if params[param_key] < 0 or isinstance(params[param_key], str):
            raise ValueError("The parameter *{}* must be "
                             "non-negative and also not string".format(param_key))

    @classmethod
    def set_parameters(cls, params):
        """This method sets the parameter for the landscape types.

        Parameter:
        ----------
            params: list
                List with the landscape's parameters.
        """
        cls.verify_parameters(params)
        cls.verify_non_valid_parameters('f_max', params)
        cls.parameters.update(params)
