"""
This is a small example for how to plot and update histograms.

Different from the spontaneous presentation in the afternoon session
on Thursday, this uses stairs() instead of steps(), which is better
suited for plotting histograms, which have n+1 bin edges for n bins.
"""

import matplotlib.pyplot as plt
import numpy as np
import random

num_data = 1000     # number of random data points per trial
seed = 12345

bin_max = 1         # histogram spans [0, bin_max]
bin_width = 0.05    # width of individual bin
y_max = 120

# Bin edges are [0, bin_width, 2 * bin_width, ..., bin_max]
# Add bin_width/2 to upper limit to ensure bin_max is included in array
bin_edges = np.arange(0, bin_max+bin_width/2, bin_width)

# Prepare histogram lines as plots where all values are zero.
# The stairs() function is specially made for histograms and has the
# following properties:
#    - The *first* argument are y-values (histogram height)
#    - The *second* argument are the x-values (edges between bins)
#    - The y-values have one element less than the x-values, because
#      n bins have a total of n+1 edges.
#    - The return value is a StepPatch, not a line object.
# See also https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.stairs.html
#
# We need to call stairs() once for each line we want to have in the histogram.

fig = plt.figure()
ax = plt.subplot(1, 1, 1)
hist_counts = np.zeros_like(bin_edges[:-1], dtype=float)
hist_uni = ax.stairs(hist_counts, bin_edges, color='r', lw=2, label='Uni')
hist_nrm = ax.stairs(hist_counts, bin_edges, color='b', lw=2, label='Norm')
ax.set_ylim([0, y_max])
ax.legend()

# Now run a "simulation", where we draw uniform random numbers for the one line
# and normal-distributed numbers for the other line. Obtain histogram counts using
# numpy.histogram(). Ignore the second return argument, which is identical to the
# bin_edges we provide as input. Then update the data in the histogram lines using
# set_data().
random.seed(seed)
for _ in range(20):
    data_uni = [random.random() for _ in range(num_data)]
    hist_counts_uni, _ = np.histogram(data_uni, bin_edges)
    hist_uni.set_data(hist_counts_uni)

    data_nrm = [random.normalvariate(0.5, 0.2) for _ in range(num_data)]
    hist_counts_nrm, _ = np.histogram(data_nrm, bin_edges)
    hist_nrm.set_data(hist_counts_nrm)

    plt.pause(0.5)
