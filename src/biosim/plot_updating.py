"""
Brief illustration of re-plotting vs data-updating.
"""

import matplotlib.pyplot as plt
import numpy as np
import random


def replot(max_step, step_size=1, linestyle='b-'):
    """
    Naive function plotting a curve one data point at a time.

    This function calls plot() for each new data point added, leading to
    increasingly slower figure updates.

    Parameters
    ----------
    max_step : int
        number of steps to plot
    step_size : int
        interval between steps to plot, default: 1
    linestyle : str
        line style specification
    """

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.set_title('Replot')
    ax.set_xlim(0, max_step)
    ax.set_ylim(0, 1)

    random.seed(12345)
    xdata = []
    ydata = []
    for n in range(0, max_step, step_size):
        xdata.append(n)
        ydata.append(random.random())
        ax.plot(xdata, ydata, linestyle)
        fig.canvas.flush_events()
        plt.pause(1e-6)


def update_in_place_v1(max_step, step_size=1, linestyle='b-'):
    """
    Plot function one point at a time by updating plot data.

    This function calls plot() only once, setting all x-data and filling
    y-data with NaN values. y-data is then updated to add each new data
    point.

    Notes
    -----
    For `step_size > 1`, nothing will be shown unless the line style includes
    markers. This happens because Matplotlib does not draw lines across NaN
    values. See `update_append()` for an alternative.

    Parameters
    ----------
    max_step : int
        last step to plot
    step_size : int
        interval between steps to plot, default: 1
    linestyle : str
        line style specification
    """

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.set_title('update_in_place_v1')
    ax.set_xlim(0, max_step)
    ax.set_ylim(0, 1)

    line = ax.plot(np.arange(max_step),
                   np.full(max_step, np.nan), linestyle)[0]

    random.seed(12345)
    for n in range(0, max_step, step_size):
        ydata = line.get_ydata()
        ydata[n] = random.random()
        line.set_ydata(ydata)
        plt.pause(1e-6)


def update_in_place(max_step, step_size=1, linestyle='b-'):
    """
    Plot function one point at a time by updating plot data.

    This function calls plot() only once, setting all x-data and filling
    y-data with NaN values. y-data is then updated to add each new data
    point.

    Parameters
    ----------
    max_step : int
        last step to plot
    step_size : int
        interval between steps to plot, default: 1
    linestyle : str
        line style specification
    """

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.set_title('update_in_place')
    ax.set_xlim(0, max_step)
    ax.set_ylim(0, 1)

    # Create line with x- and y-data only for points to be plotted.
    # Ensure that all y-data has same size as x-data. Since xdata
    # most likely has data type int, we need to force float for y-data,
    # since full_like() copies data type by default.
    xdata = np.arange(0, max_step, step_size)
    line = ax.plot(xdata,
                   np.full_like(xdata, np.nan, dtype=float), linestyle)[0]

    random.seed(12345)
    for n in range(0, max_step, step_size):
        idx = n // step_size    # integer division to get correct array location
        ydata = line.get_ydata()
        ydata[idx] = random.random()
        line.set_ydata(ydata)
        plt.pause(1e-6)


if __name__ == '__main__':

    total_steps = 350
    stepping = 1
    style = 'b-'
    replot(total_steps, stepping, style)
    #update_in_place_v1(total_steps, stepping, style)
    #update_in_place(total_steps, stepping, style)

    plt.show()
