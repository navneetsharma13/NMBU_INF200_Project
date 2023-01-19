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

    def init_plot(self, num_years,map_str=None):

        self.y_herb = [np.nan for i in range(num_years + 1)]
        self.y_carn = [np.nan for i in range(num_years + 1)]

        print(self.y_herb)
        print(self.y_carn)

        fig = plt.figure(figsize=(10, 7), constrained_layout=True)  # Initiate pyplot
        gs = fig.add_gridspec(4, 6)

        self.ax_main = fig.add_subplot(gs[:2, :])  # Add the main subplot
        self.ax_weight = fig.add_subplot(gs[2, :2])  # Add weight subplot
        self.ax_fitness = fig.add_subplot(gs[2, 2:4])  # Add fitness subplot
        self.ax_age = fig.add_subplot(gs[2, 4:])  # Add age subplot
        self.axhm_herb = fig.add_subplot(gs[3, :2])  # Add herb heatmap subplot
        self.axhm_carn = fig.add_subplot(gs[3, 2:4])  # Add carn heatmap subplot
        self.ax_im = fig.add_subplot(gs[3, -2:-1])  # Add map subplot
        self.ax_lg = fig.add_subplot(gs[3, -1])  # Add map legend subplot
        self.plot_map(map_str)
        #self.plot_heatmap()

        (self.herb_line,) = self.ax_main.plot(self.y_herb)  # Initiate the herbivore line
        (self.carn_line,) = self.ax_main.plot(self.y_carn)  # Initiate the carnivore line

        self.ax_main.legend(["Herbivore count", "Carnivore count"])  # Insert legend into plot
        self.ax_main.set_xlabel("Simulation year")  # Define x-label
        self.ax_main.set_ylabel("Animal count")  # Define y-label
        self.ax_main.set_xlim(
            [0, num_years]
        )  # x-limit is set permanently to amount of years to simulate

        if self.ymax is not None:
            self.ax_main.set_ylim([0, self.ymax])

        plt.ion()  # Activate interactive mode

    def set_x_axis(self, years_target):
        self.ax_main.set_xlim([0, years_target])  # Update x_limit when several simulations are run

    def update_plot(self):

        if self.ymax is None:
            if max(self.y_herb) >= max(
                    self.y_carn
            ):  # Find the biggest count value in either y_herb or y_carn
                self.ax_main.set_ylim([0, max(self.y_herb) + 20])  # Set y-lim
            else:
                self.ax_main.set_ylim([0, max(self.y_carn) + 20])  # Set y-lim

        # if self.island.get_pop_tot_num_carn() > 0 or self.island.get_pop_tot_num_herb() > 0:
        #     weight_data = [[12,23,34,12,34,34],[12,23,34,12,34,34]]
        #     weight_max = int(max(max(weight_data)))
        #     weight_min = int(min(min(weight_data)))
        #     weight_delta = self.hist_specs["weight"]["delta"]
        #     self.ax_weight.clear()
        #     self._weight_hist = self.ax_weight.hist(
        #         weight_data, range(weight_min, weight_max + int(weight_delta), weight_delta),
        #     )
        #     self.ax_weight.set_xlim([0, self.hist_specs["weight"]["max"]])

            # fitness_data = self.island.animal_fitness
            # fitness_delta = self.hist_specs["fitness"]["delta"]
            #
            # self.ax_fitness.clear()
            # self.ax_fitness.hist(fitness_data, bins=np.arange(0, 1 + fitness_delta, fitness_delta))
            #
            # self.ax_fitness.set_xlim([0, self.hist_specs["fitness"]["max"]])
            #
            # age_data = self.island.animal_ages
            # age_max = int(max(max(age_data)))
            # age_min = int(min(min(age_data)))
            # age_delta = self.hist_specs["age"]["delta"]
            # self.ax_age.clear()
            # self.ax_age.hist(age_data, bins=range(age_min, age_max + int(age_delta), age_delta))
            # self.ax_age.set_xlim([0, self.hist_specs["age"]["max"]])

            self.herb_line.set_ydata(self.y_herb)
            self.herb_line.set_xdata(range(len(self.y_herb)))
            self.carn_line.set_ydata(self.y_carn)
            self.carn_line.set_xdata(range(len(self.y_carn)))

            self.ax_weight.set_title("Weight distribution")
            self.ax_fitness.set_title("Fitness distribution")
            self.ax_age.set_title("Age distribution")

        self.imax_herb.set_data(self.island.herb_pop_matrix)
        self.imax_carn.set_data(self.island.carn_pop_matrix)

        plt.pause(1e-6)

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

        self.ax_im = fig.add_axes([0.1, 0.1, 0.7, 0.8])  # llx, lly, w, h

        self.ax_im.imshow(plot_rgb)
        self.ax_im.set_xticks(range(len(plot_rgb[0])))
        self.ax_im.set_xticklabels(range(1, 1 + len(plot_rgb[0])))
        self.ax_im.set_yticks(range(len(plot_rgb)))
        self.ax_im.set_yticklabels(range(1, 1 + len(plot_rgb)))

        # for label in self.ax_im.xaxis.get_ticklabels()[1::2]:
        #     label.set_visible(False)

        self.ax_lg = fig.add_axes([0.85, 0.1, 0.1, 0.8])  # llx, lly, w, h
        self.ax_lg.axis('off')

        for ix, name in enumerate(('Water', 'Lowland',
                                   'Highland', 'Desert')):
            self.ax_lg.add_patch(plt.Rectangle((0., ix * 0.2), 0.3, 0.1,
                                               edgecolor='none',
                                               facecolor=rgb_value[name[0]]))
            self.ax_lg.text(0.35, ix * 0.2, name, transform=self.ax_lg.transAxes)

        plt.show()

    def plot_heatmap(self):

        # self.herb_pop_matrix = [[0 for _ in self.island.unique_columns()] for _ in self.island.unique_rows()]
        # self.carn_pop_matrix = [[0 for _ in self.island.unique_columns()] for _ in self.island.unique_rows()]


        self.imax_herb = self.axhm_herb.imshow(
            self.island.herb_pop_matrix,
            cmap="viridis",
            interpolation="nearest",
            vmax=self.cmax_herb,
        )
        self.imax_carn = self.axhm_carn.imshow(
            self.island.carn_pop_matrix,
            cmap="cividis",
            interpolation="nearest",
            vmax=self.cmax_carn,
        )
        self.axhm_herb.set_title("Herbivore density")
        self.axhm_carn.set_title("Carnivore density")

        plt.colorbar(self.imax_herb, ax=self.axhm_herb, orientation="vertical")

        plt.colorbar(self.imax_carn, ax=self.axhm_carn, orientation="vertical")

        plt.show()


    def save_graphics(self,img_base,img_fmt):
        if img_base is None:
            return
        plt.savefig("{base}_{num:05d}.{type}".format(base=img_base, num=self.img_ctr, type=img_fmt))
        self.img_ctr += 1