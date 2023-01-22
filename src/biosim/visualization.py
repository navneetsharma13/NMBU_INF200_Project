import matplotlib.pyplot as plt
import numpy as np


class Visualization:

    def __init__(self, island_map=None, cmax=None, ymax=None, hist_specs=None, total_years=None,
                 pop_matrix_herb=None, pop_matrix_carn=None, img_base=None, img_fmt=None):

        self.island_map = island_map
        self.img_base = img_base
        self.img_ctr = 0
        self.img_year = 1
        self.img_fmt = img_fmt
        self.total_years = None
        self.y_herb = None
        self.y_carn = None
        self.herb_line = None
        self.carn_line = None
        self.fitness_hist_herb = None
        self.fitness_hist_carn = None
        self.age_hist_herb = None
        self.age_hist_carn = None
        self.weight_hist_herb = None
        self.weight_hist_carn = None
        self.bin_edges_fitness = None
        self.bin_edges_age = None
        self.bin_edges_weight = None
        self.txt = None
        self.template = None
        self.herb_fitness_list = None
        self.carn_fitness_list = None
        self.axt = None
        self.ax_main = None
        self.ax_animal_count = None
        self.ax_weight = None
        self.ax_fitness = None
        self.ax_age = None
        self.weight_hist = None
        self.fitness_hist = None
        self.age_hist = None
        self.ax_hm_herb = None
        self.imax_herb = None
        self.ax_hm_carn = None
        self.imax_carn = None
        self.ax_im = None
        self.ax_lg = None
        self.weight_carn_list = None
        self.age_carn_list = None
        self.fitness_carn_list = None
        self.weight_herb_list = None
        self.age_herb_list = None
        self.fitness_herb_list = None
        self.herb_hm_axis = None
        self.carn_hm_axis = None
        self.pop_matrix_herb = pop_matrix_herb
        self.pop_matrix_carn = pop_matrix_carn

        if total_years is None:
            self.total_years = 0
        else:
            self.total_years = total_years

        if ymax is None:
            self.ymax = 20000
        else:
            self.ymax = ymax

        if cmax is None:
            self.cmax = {"Herbivore": 150, "Carnivore": 60}
        else:
            self.cmax = cmax

        if hist_specs is None:
            self.hist_specs = {
                "weight": {"max": 80, "delta": 2},
                "fitness": {"max": 1.0, "delta": 0.05},
                "age": {"max": 60, "delta": 2},
            }
        else:
            self.hist_specs = hist_specs

    def draw_layout(self):

        fig = plt.figure(figsize=(12, 8), constrained_layout=True)  # Setup pyplot

        plt.get_current_fig_manager().full_screen_toggle()  # maximizing plot size to fullscreen

        gs = fig.add_gridspec(5, 7)

        self.ax_lg = fig.add_subplot(gs[0, 0])  # Add map legend subplot
        self.ax_im = fig.add_subplot(gs[0:2, 1:3])
        self.ax_animal_count = fig.add_subplot(gs[0:2, 3:])
        self.ax_hm_herb = fig.add_subplot(gs[2:4, 1:3])
        self.axt = fig.add_subplot(gs[0, 4])
        self.ax_hm_carn = fig.add_subplot(gs[2:4, 3:5])
        self.ax_fitness = fig.add_subplot(gs[4:, 1:3])
        self.ax_age = fig.add_subplot(gs[4:, 3:5])
        self.ax_weight = fig.add_subplot(gs[4:, 5:])

        self.draw_map()
        self.draw_animal_count_plot()
        self.draw_frequency_graphs()
        self.draw_heatmap()

        self.ax_hm_herb.set_title('Herbivore Distribution')
        self.ax_hm_carn.set_title('Carnivore Distribution')
        self.ax_fitness.set_title('Fitness Frequency')
        self.ax_age.set_title('Age Frequency')
        self.ax_weight.set_title('Weight Frequency')

    def draw_map(self):
        """Author: Hans E. Plasser"""

        rgb_value = {
            #      R    G    B
            "W": (0.0, 0.0, 1.0),  # blue
            "L": (0.0, 0.6, 0.0),  # dark green
            "H": (0.5, 1.0, 0.5),  # light green
            "D": (1.0, 1.0, 0.5),  # light yellow
        }

        plot_rgb = [[rgb_value[column] for column in row.strip()] for row in
                    self.island_map.splitlines()]

        self.ax_im.imshow(plot_rgb)
        self.ax_im.set_xticks(range(len(plot_rgb[0])))
        self.ax_im.set_xticklabels(range(1, 1 + len(plot_rgb[0])))
        self.ax_im.set_yticks(range(len(plot_rgb)))
        self.ax_im.set_yticklabels(range(1, 1 + len(plot_rgb)))

        self.ax_im.axis("off")  # for removing the axes coordinates
        for label in self.ax_im.xaxis.get_ticklabels()[1::2]:
            label.set_visible(False)

        self.ax_lg.axis("off")
        for ix, name in enumerate(("Water", "Lowland", "Highland", "Desert")):
            self.ax_lg.add_patch(
                plt.Rectangle(
                    (0.0, ix * 0.2), 0.3, 0.1, edgecolor="none", facecolor=rgb_value[name[0]]
                )
            )
            self.ax_lg.text(0.35, ix * 0.2, name, transform=self.ax_lg.transAxes)

        self.axt.axis('off')
        self.template = 'Year: {:5d}'
        self.txt = self.axt.text(0.5, 0.5, self.template.format(0), horizontalalignment='center',
                                 verticalalignment='center', transform=self.axt.transAxes)

    def draw_animal_count_plot(self):

        num_years = self.total_years
        self.ax_animal_count.set_title("Animal Count")
        self.ax_animal_count.set_xlim(0, num_years)
        self.ax_animal_count.set_ylim([0, self.ymax])

        step_size = 1
        linestyle = 'b-'
        animal_xdata = np.arange(0, num_years, step_size)
        self.herb_line = self.ax_animal_count.plot(animal_xdata,
                                                   np.full_like(animal_xdata,
                                                                np.nan, dtype=float), linestyle)[0]
        self.carn_line = self.ax_animal_count.plot(animal_xdata,
                                                   np.full_like(animal_xdata,
                                                                np.nan, dtype=float),
                                                   linestyle, color='r')[0]

        self.ax_animal_count.legend(["Herbivore Count", "Carnivore Count"])
        self.ax_animal_count.set_xlabel("Simulation Year")
        self.ax_animal_count.set_ylabel("Herbivore and Carnivore Count")

    def draw_frequency_graphs(self):

        # fitness Frequency Graph
        bin_max_fitness = self.hist_specs["fitness"]["max"]  # histogram spans [0, bin_max]
        bin_width_fitness = self.hist_specs["fitness"]["delta"]  # width of individual bin
        self.bin_edges_fitness = np.arange(0, bin_max_fitness + bin_width_fitness / 2,
                                           bin_width_fitness)
        hist_counts_fitness = np.zeros_like(self.bin_edges_fitness[:-1], dtype=float)
        self.fitness_hist_herb = self.ax_fitness.stairs(hist_counts_fitness, self.bin_edges_fitness,
                                                        color='b',
                                                        lw=2,
                                                        label='Herbivore')
        self.fitness_hist_carn = self.ax_fitness.stairs(hist_counts_fitness, self.bin_edges_fitness,
                                                        color='r',
                                                        lw=2,
                                                        label='Carnivore')

        # age Frequency Graph
        bin_max_age = self.hist_specs["age"]["max"]  # histogram spans [0, bin_max]
        bin_width_age = self.hist_specs["age"]["delta"]  # width of individual bin
        self.bin_edges_age = np.arange(0, bin_max_age + bin_width_age / 2, bin_width_age)
        hist_counts_age = np.zeros_like(self.bin_edges_age[:-1], dtype=float)
        self.age_hist_herb = self.ax_age.stairs(hist_counts_age, self.bin_edges_age,
                                                color='b', lw=2,
                                                label='Herbivore')
        self.age_hist_carn = self.ax_age.stairs(hist_counts_age, self.bin_edges_age,
                                                color='r', lw=2,
                                                label='Carnivore')

        # weight Frequency Graph
        bin_max_weight = self.hist_specs["weight"]["max"]  # histogram spans [0, bin_max]
        bin_width_weight = self.hist_specs["weight"]["delta"]  # width of individual bin
        self.bin_edges_weight = np.arange(0, bin_max_weight + bin_width_weight / 2,
                                          bin_width_weight)
        hist_counts_weight = np.zeros_like(self.bin_edges_weight[:-1], dtype=float)
        self.weight_hist_herb = self.ax_weight.stairs(hist_counts_weight, self.bin_edges_weight,
                                                      color='b', lw=2,
                                                      label='Herbivore')
        self.weight_hist_carn = self.ax_weight.stairs(hist_counts_weight, self.bin_edges_weight,
                                                      color='r', lw=2,
                                                      label='Carnivore')

    def draw_heatmap(self):

        self.herb_hm_axis = self.ax_hm_herb.imshow(self.pop_matrix_herb, interpolation='nearest',
                                                   cmap='viridis', vmin=0, vmax=self.cmax["Herbivore"])
        plt.colorbar(self.herb_hm_axis, ax=self.ax_hm_herb, orientation='vertical',
                     fraction=0.028, )

        self.carn_hm_axis = self.ax_hm_carn.imshow(self.pop_matrix_carn, interpolation='nearest',
                                                   cmap='plasma', vmin=0, vmax=self.cmax["Carnivore"])
        plt.colorbar(self.carn_hm_axis, ax=self.ax_hm_carn, orientation='vertical', fraction=0.028)

    def update_plot(self, pop_herb=0, pop_carn=0, step_size=1, current_year=0,
                    pop_matrix_herb=None, pop_matrix_carn=None, weight_list=None,
                    age_list=None, fitness_list=None):

        self.fitness_herb_list = fitness_list['Herbivore']
        self.age_herb_list = age_list['Herbivore']
        self.weight_herb_list = weight_list['Herbivore']

        self.fitness_carn_list = fitness_list['Carnivore']
        self.age_carn_list = age_list['Carnivore']
        self.weight_carn_list = weight_list['Carnivore']

        self.pop_matrix_herb = pop_matrix_herb
        self.pop_matrix_carn = pop_matrix_carn

        self.txt.set_text(self.template.format(current_year))

        self.update_animal_count(pop_herb=pop_herb, pop_carn=pop_carn,
                                 step_size=step_size, current_year=current_year)
        self.update_frequency_graphs()
        self.update_heatmap()
        plt.pause(0.05)

    def update_animal_count(self, pop_herb=0, pop_carn=0, step_size=1, current_year=0):

        n = current_year
        idx = n // step_size
        herb_ydata = self.herb_line.get_ydata()  # plotting of ydata for herb
        herb_ydata[idx] = pop_herb
        self.herb_line.set_ydata(herb_ydata)

        carn_ydata = self.carn_line.get_ydata()  # plotting of ydata for carn
        carn_ydata[idx] = pop_carn
        self.carn_line.set_ydata(carn_ydata)

    def update_frequency_graphs(self):

        fitness_hist_counts_herb, _ = np.histogram(self.fitness_herb_list, self.bin_edges_fitness)
        self.fitness_hist_herb.set_data(fitness_hist_counts_herb)
        fitness_hist_counts_carn, _ = np.histogram(self.fitness_carn_list, self.bin_edges_fitness)
        self.fitness_hist_carn.set_data(fitness_hist_counts_carn)
        y_max_fitness = max(max(fitness_hist_counts_herb), max(fitness_hist_counts_carn)) + 20
        self.ax_fitness.set_ylim([0, y_max_fitness])

        age_hist_counts_herb, _ = np.histogram(self.age_herb_list, self.bin_edges_age)
        self.age_hist_herb.set_data(age_hist_counts_herb)
        age_hist_counts_carn, _ = np.histogram(self.age_carn_list, self.bin_edges_age)
        self.age_hist_carn.set_data(age_hist_counts_carn)
        y_max_age = max(max(age_hist_counts_herb), max(age_hist_counts_carn)) + 20
        self.ax_age.set_ylim([0, y_max_age])

        weight_hist_counts_herb, _ = np.histogram(self.weight_herb_list, self.bin_edges_weight)
        self.weight_hist_herb.set_data(weight_hist_counts_herb)
        weight_hist_counts_carn, _ = np.histogram(self.weight_carn_list, self.bin_edges_weight)
        self.weight_hist_carn.set_data(weight_hist_counts_carn)
        y_max_weight = max(max(weight_hist_counts_herb), max(weight_hist_counts_carn)) + 20
        self.ax_weight.set_ylim([0, y_max_weight])

    def update_heatmap(self):
        self.herb_hm_axis.set_data(self.pop_matrix_herb)
        self.carn_hm_axis.set_data(self.pop_matrix_carn)

    def save_graphics(self, step):
        """Saves graphics to file if file name given."""

        if self.img_base is None or step % self.img_year != 0:
            return

        plt.savefig('{base}_{num:05d}.{type}'.format(base=self.img_base,
                                                     num=self.img_ctr,
                                                     type=self.img_fmt))

        self.img_ctr += 1
