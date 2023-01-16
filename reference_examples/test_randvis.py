#!/usr/bin/env python

"""
This is a small demo script running a randvis simulation.
"""

import matplotlib.pyplot as plt
from src.biosim.simulation import BioSim

if __name__ == '__main__':

    sim = BioSim((10, 15), 0.1, seed=12345)
    sim.simulate(250, 1, 5)

    print('Close the figure to end the program!')

    plt.show()
