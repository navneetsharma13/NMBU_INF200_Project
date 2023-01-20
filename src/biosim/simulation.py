import random
from .map import Map
import sys
import csv
import numpy as np
from src.biosim.visualization import Visualization

"""
Template for BioSim class.
"""


# The material in this file is licensed under the BSD 3-clause license
# https://opensource.org/licenses/BSD-3-Clause
# (C) Copyright 2023 Hans Ekkehard Plesser / NMBU


class BioSim:
    """
    Top-level interface to BioSim package.
    """

    def __init__(self, island_map, ini_pop, seed,
                 vis_years=1, ymax_animals=None, cmax_animals=None, hist_specs=None,
                 img_years=None, img_dir=None, img_base=None, img_fmt='png', plot_graph=True,
                 log_file=None, total_years=0):

        """
        Parameters
        ----------
        island_map : str
            Multi-line string specifying island geography
        ini_pop : list
            List of dictionaries specifying initial population
        seed : int
            Integer used as random number seed
        vis_years : int
            Years between visualization updates (if 0, disable graphics)
        ymax_animals : int
            Number specifying y-axis limit for graph showing animal numbers
        cmax_animals : dict
            Color-scale limits for animal densities, see below
        hist_specs : dict
            Specifications for histograms, see below
        img_years : int
            Years between visualizations saved to files (default: `vis_years`)
        img_dir : str
            Path to directory for figures
        img_base : str
            Beginning of file name for figures
        img_fmt : str
            File type for figures, e.g. 'png' or 'pdf'
        log_file : str
            If given, write animal counts to this file

        Notes
        -----
        - If `ymax_animals` is None, the y-axis limit should be adjusted automatically.
        - If `cmax_animals` is None, sensible, fixed default values should be used.
        - `cmax_animals` is a dict mapping species names to numbers, e.g.,

          .. code:: python

             {'Herbivore': 50, 'Carnivore': 20}

        - `hist_specs` is a dictionary with one entry per property for which a histogram
          shall be shown. For each property, a dictionary providing the maximum value
          and the bin width must be given, e.g.,

          .. code:: python

             {'weight': {'max': 80, 'delta': 2},
              'fitness': {'max': 1.0, 'delta': 0.05}}

          Permitted properties are 'weight', 'age', 'fitness'.
        - If `img_dir` is None, no figures are written to file.
        - Filenames are formed as

          .. code:: python

             Path(img_dir) / f'{img_base}_{img_number:05d}.{img_fmt}'

          where `img_number` are consecutive image numbers starting from 0.

        - `img_dir` and `img_base` must either be both None or both strings.
        """
        self.island_map = island_map
        self.map = Map(island_map)
        self.map.add_population(ini_pop)
        random.seed(seed)
        self.last_year = 0
        self.year_num = 0
        self.img_no = 0
        self.final_year = None
        self.img_fmt = img_fmt
        self.fig = None
        self.img_axis = None
        self.mean_ax = None
        self.herbivore_line = None
        self.plot_bool = plot_graph
        self.log_file = log_file
        self.hist_specs = hist_specs
        self.csvfile = None
        self.writer = None

        if img_base is None:
            self.img_base = None
        else:
            self.img_base = img_base

        if ymax_animals is None:
            self.ymax_animals = None
        else:
            self.ymax_animals = ymax_animals

        if cmax_animals is None:
            self.cmax_animals = None
        else:
            self.cmax_animals = cmax_animals

        if self.plot_bool:
            self.visualize = Visualization(self.island_map, cmax=self.cmax_animals,
                                           ymax=self.ymax_animals,
                                           hist_specs=self.hist_specs,
                                           total_years=total_years,
                                           pop_matrix_herb=self.map.get_pop_matrix_herb(),
                                           pop_matrix_carn=self.map.get_pop_matrix_carn())
            self.visualize.draw_layout()

    def set_animal_parameters(self, species, params):
        """
        Set parameters for animal species.

        Parameters
        ----------
        species : str
            Name of species for which parameters shall be set.
        params : dict
            New parameter values

        Raises
        ------
        ValueError
            If invalid parameter values are passed.
        """
        self.map.set_parameters(species, params)

    def set_landscape_parameters(self, landscape, params):
        """
        Set parameters for landscape type.

        Parameters
        ----------
        landscape : str
            Code letter for landscape
        params : dict
            New parameter values

        Raises
        ------
        ValueError
            If invalid parameter values are passed.
        """
        self.map.set_parameters(landscape, params)

    def simulate(self, num_years, vis_years=1, img_years=None):
        """
        Run simulation while visualizing the result.

        Parameters
        ----------
        num_years : int
            Number of years to simulate
        vis_years : interval between visualization updates
        img_years: interval between visualizations saved to files
                          (default: vis_years)

        .. note:: Image files will be numbered consecutively.
        """

        if img_years is None:
            img_years = vis_years

        if img_years % vis_years != 0:
            raise ValueError('img_years must be multiple of vis_years')

        self.final_year = self.year_num + num_years
        self.csvfile = open(f"{sys.path[1]}/{self.log_file}", 'a', newline="")
        self.writer = csv.writer(self.csvfile, delimiter=',')
        while self.year_num < self.final_year:
            self.map.yearly_cycle()
            self.visualize.update_plot_population(pop_herb=self.map.get_pop_tot_num_herb(),
                                           pop_carn=self.map.get_pop_tot_num_carn(),
                                           step_size=1,
                                           current_year=self.year_num,
                                           pop_matrix_herb=self.map.get_pop_matrix_herb(),
                                           pop_matrix_carn=self.map.get_pop_matrix_carn(),
                                           weight_list=self.weight_animals_per_species(),
                                           age_list=self.age_animals_per_species(),
                                           fitness_list=self.fitness_animals_per_species())

            # if self.img_base is not None:
            #     if img_years is None:
            #         if self.year_num % vis_years==0:
            #             self.plot.save_graphics(self.img_base,self.img_fmt)
            #     else:
            #         if self.year_num % img_years ==0:
            #             self.plot.save_graphics(self.img_base,self.img_fmt)

            self.writer.writerow(
                [self.year_num, self.map.get_pop_tot_num_herb(), self.map.get_pop_tot_num_carn()])

            self.year_num += 1

    def plot_show_sim(self):
        self.visualize.show_plot()

    def plot_close_sim(self):
        self.visualize.close_plot()

    def add_population(self, population):
        """
        Add a population to the island

        Parametersu
        ----------
        population : List of dictionaries
            See BioSim Task Description, Sec 3.3.3 for details.
        """
        self.map.add_population(population)

    @property
    def year(self):
        """Last year simulated."""
        return self.last_year

    @property
    def num_animals(self):
        """Total number of animals on island."""
        return self.map.get_pop_tot_num_carn() + self.map.get_pop_tot_num_herb()

    @property
    def num_animals_per_species(self):
        """Number of animals per species in island, as dictionary."""
        return {'Herbivore': self.map.get_pop_tot_num_herb(),
                'Carnivore': self.map.get_pop_tot_num_carn()}

    def age_animals_per_species(self):
        """Number of animals per species in island, as dictionary."""
        return {'Herbivore': self.map.get_pop_age_herb(),
                'Carnivore': self.map.get_pop_age_carn()}

    def weight_animals_per_species(self):
        """Number of animals per species in island, as dictionary."""
        return {'Herbivore': self.map.get_pop_weight_herb(),
                'Carnivore': self.map.get_pop_weight_carn()}

    def fitness_animals_per_species(self):
        """Number of animals per species in island, as dictionary."""
        return {'Herbivore': self.map.get_pop_fitness_herb(),
                'Carnivore': self.map.get_pop_fitness_carn()}

    def make_movie(self):
        """Create MPEG4 movie from visualization images saved."""

    def run(self, cycles, report_cycles=1, return_counts=False):
        """
        Run simulation for given number of cycles.

        Parameters
        ----------
        cycles : int
            number of cycles to simulate
        report_cycles : int
            interval between status information updates (== 0: no output)
        return_counts : int
            if True, return population counts
        Returns
        -------
        None or tuple
            If return of counts is requested, a tuple (cycle, Herb Count, Carn Count)
        """
        disp = report_cycles > 0
        ret = return_counts

        if ret:
            data = np.empty((cycles + 1, 3))
            data[:, 0] = range(cycles + 1)
            data[1] = self.map.get_pop_tot_num_herb()
            data[2] = self.map.get_pop_tot_num_carn()
        else:
            data = None

        if disp:
            print('Start: Herbivores', self.map.get_pop_tot_num_herb())
            print('Start: Carnivores', self.map.get_pop_tot_num_carn())

        for cycle in range(cycles):
            self.map.yearly_cycle()
            disp_this_cycle = disp and cycle % report_cycles == 0

            if ret or disp_this_cycle:
                n_a, n_b = self.map.get_pop_tot_num_herb(), self.map.get_pop_tot_num_carn()
                if ret:
                    data[cycle + 1, 1:] = n_a, n_b
                if disp_this_cycle:
                    print(n_a, n_b)

        if disp:
            print('End: Herbivore', self.map.get_pop_tot_num_herb())
            print('End: Carnivore', self.map.get_pop_tot_num_carn())

        if ret:
            return data
