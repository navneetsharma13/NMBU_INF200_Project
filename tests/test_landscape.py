"""
This is the geography pytest package which is a test package for the  BioSim packages written for
 the INF200 project January 2022.
"""

__author__ = "Navneet Sharma and Sushant Kumar Srivastava"
__email__ = "navneet.sharma@nmbu.no and sushant.kumar.sirvastava@nmbu.no"

import pytest
import random as rd
import numpy as np
from src.biosim.landscape import Lowland, Highland


def test_verify_unknown_parameters():
    """Test method 'verify_parameters()' if it does not identify the given parameter as incorrect
     and return ValueError"""
    with pytest.raises(ValueError):
        Lowland.verify_parameters(params={'f_min': 100})
        Highland.verify_parameters(params={'f_min': 100})


def test_verify_known_parameters():
    """Test method 'verify_parameters()' if it does not identify the given parameter are correct and
     returns ValueError"""
    Lowland.verify_parameters(params={'f_max': 100})
    Highland.verify_parameters(params={'f_max': 100})


def test_negative_parameters():
    """Test method 'verify_non_valid_parameters(param_key, params)' if it identifies the
    negative value of a given parameter and returns ValueError"""
    param_key, params = 'f_max', {'f_max': -344}
    with pytest.raises(ValueError):
        Lowland.verify_non_valid_parameters(param_key, params)
        Highland.verify_non_valid_parameters(param_key, params)


def test_string_parameters():
    """Test method 'verify_non_valid_parameters(param_key, params)' if it identifies the
    negative value of a given parameter and returns ValueError"""
    param_key, params = 'f_max', {'f_max': "sadsa"}
    with pytest.raises(ValueError):
        Lowland.verify_non_valid_parameters(param_key, params)
        Highland.verify_non_valid_parameters(param_key, params)
