import matplotlib.pyplot as plt
import numpy as np
import random
from src.biosim.map import Map

class Plotting:

    def __init__(self, island_map, cmax=None, ymax=None, hist_specs=None):
        self.island = Map(island_map)
        self.img_base = None
        self.img_ctr = 0

        self.y_herb = None
        self.y_carn = None
        self.herb_line = None
        self.carn_line = None
        self.herb_fitness_list = None
        self.carn_fitness_list = None
        self.ax_main = None
        self.ax_weight = None
        self.ax_fitness = None
        self.ax_age = None
        self.weight_hist = None
        self.fitness_hist = None
        self.age_hist = None
        self.axhm_herb = None
        self.imax_herb = None
        self.axhm_carn = None
        self.imax_carn = None
        self.ax_im = None
        self.ax_lg = None

        self.ymax = ymax
        self.cmax = cmax

        if self.cmax is None:
            self.cmax = {"Herbivore": 200, "Carnivore": 50}

        self.cmax_herb = self.cmax["Herbivore"]
        self.cmax_carn = self.cmax["Carnivore"]

        if hist_specs is None:
            self.hist_specs = {
                "weight": {"max": 80, "delta": 2},
                "fitness": {"max": 1.0, "delta": 0.05},
                "age": {"max": 80, "delta": 2},
            }
        else:
            self.hist_specs = hist_specs

        self.ax_carn=None
    def plot_map(self, island_str):

        """Author: Hans E. Plasser
        :param map_str: Multi-line string containing letters symbolizing the landscape
        :type map_str: str
        """
        rgb_value = {
            "W": (0.0, 0.0, 1.0),  # blue
            "L": (0.0, 0.6, 0.0),  # dark green
            "H": (0.5, 1.0, 0.5),  # light green
            "D": (1.0, 1.0, 0.5),  # light yellow
        }

        plot_rgb = [[rgb_value[column] for column in row.strip()] for row in island_str.splitlines()]

        fig = plt.figure()
        self.ax_im = fig.add_subplot(2, 2, 1)
        self.ax_carn = fig.add_subplot(2, 2,2)
        self.ax_herb = fig.add_subplot(2, 2, 3)
        self.ax3 = fig.add_subplot(2, 2, 4)
        # self.ax4 = fig.add_subplot(2, 3, 5)
        # self.ax5 = fig.add_subplot(2, 3, 6)


        #self.ax_im = fig.add_axes([0.05, 0.2, 0.6, 0.6])  # llx, lly, w, h

        self.ax_im.imshow(plot_rgb)
        self.ax_im.set_xticks(range(len(plot_rgb[0])))
        self.ax_im.set_xticklabels(range(1, 1 + len(plot_rgb[0])))

        self.ax_im.set_yticks(range(len(plot_rgb)))
        self.ax_im.set_yticklabels(range(1, 1 + len(plot_rgb)))

        self.ax_im.axis("off") #for removing the axes coordinates
        for label in self.ax_im.xaxis.get_ticklabels()[1::28]:
            label.set_visible(False)

        self.ax_lg = fig.add_axes([0.01,0.58, 0.04, 0.4])  # llx, lly, w, h
        self.ax_lg.axis('off') #for removing the axe coordinates

        for ix, name in enumerate(('Water', 'Lowland',
                                   'Highland', 'Desert')):
            self.ax_lg.add_patch(plt.Rectangle((0., ix * 0.2), 0.3, 0.1,
                                               edgecolor='none',
                                               facecolor=rgb_value[name[0]]))
            self.ax_lg.text(0.35, ix * 0.2, name, transform=self.ax_lg.transAxes)





    def plot_population(self):

        num_year=300
        step_size=1
        linestyle='b-'
        self.ax_carn.set_title("Population")
        self.ax_carn.set_xlim(0,num_year)
        self.ax_carn.set_ylim(0,15000)

        carn_xdata=np.arange(0,num_year,step_size)
        line = self.ax_carn.plot(carn_xdata,np.full_like(carn_xdata, np.nan, dtype=float), linestyle)[0]
        for n in range(0,num_year,step_size):
            idx=n/step_size
            ydata=line.get_ydata()
            ydata[idx]=random.random()
            line.set_ydata(ydata)
            plt.pause(1e-6)

        plt.show()