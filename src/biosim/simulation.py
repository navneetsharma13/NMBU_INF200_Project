
"""
This is the simulation model which functions with the Biosim package written for
the INF200 project January 2023.
"""

__author__ = "Navneet Sharma and Sushant Kumar Srivastava"
__email__ = "navneet.sharma@nmbu.no and sushant.kumar.srivastava@nmbu.no"

import random
import os
import glob
from biosim.map import Map
import subprocess
from biosim.visualization import Visualization

"""
Template for BioSim class.
"""

# Update these variables to point to your ffmpeg and convert binaries
# If you installed ffmpeg using conda or installed both software programs in
# standard ways on your computer, no changes should be required.
_FFMPEG_BINARY = 'ffmpeg'
_MAGICK_BINARY = 'magick'

# update this to the directory and file-name beginning
# for the graphics files
_DEFAULT_GRAPHICS_DIR = '../results'
_DEFAULT_GRAPHICS_NAME = 'dv'
_DEFAULT_IMG_FORMAT = 'png'
_DEFAULT_MOVIE_FORMAT = 'mp4'  # alternatives: mp4, gif


# The material in this file is licensed under the BSD 3-clause license
# https://opensource.org/licenses/BSD-3-Clause
# (C) Copyright 2023 Hans Ekkehard Plesser / NMBU


class BioSim:
    """
    Top-level interface to BioSim package.
    """

    def __init__(self, island_map, ini_pop, seed,
                 vis_years=1, ymax_animals=None, cmax_animals=None, hist_specs=None,
                 img_years=None, img_dir=None, img_base=None, img_fmt=None, plot_graph=True):

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
        plot_graph : boolean
            True if plot is required.
            False if plot is not required

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
        self.final_year = 0
        self.img_fmt = img_fmt
        self.fig = None
        self.img_axis = None
        self.mean_ax = None
        self.herbivore_line = None
        self.plot_bool = plot_graph
        self.hist_specs = hist_specs
        self.vis_years = vis_years
        self.visualize = None

        if vis_years == 0:
            self.plot_bool = False
        else:
            self.vis_years = vis_years

        self.img_years = img_years

        if img_dir is None:
            self.img_dir = _DEFAULT_GRAPHICS_DIR
        else:
            self.img_dir = '../'+img_dir

        if img_base is None:
            self.img_base = os.path.join(self.img_dir, _DEFAULT_GRAPHICS_NAME)
        else:
            self.img_base = os.path.join(self.img_dir, img_base)

        self.img_fmt = img_fmt if img_fmt is not None else _DEFAULT_IMG_FORMAT

        self.img_ctr = 0
        self.img_step = 1

        if ymax_animals is None:
            self.ymax_animals = None
        else:
            self.ymax_animals = ymax_animals

        if cmax_animals is None:
            self.cmax_animals = None
        else:
            self.cmax_animals = cmax_animals

        self.remove_files()

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

    def simulate(self, num_years):
        """
        Run simulation while visualizing the result.

        Parameters
        ----------
        num_years : int
            Number of years to simulate
        .. note:: Image files will be numbered consecutively.
        """

        if self.plot_bool and self.visualize is None:
            self.visualize = Visualization(self.island_map, cmax=self.cmax_animals,
                                           ymax=self.ymax_animals,
                                           hist_specs=self.hist_specs,
                                           total_years=num_years,
                                           step_size=self.vis_years,
                                           pop_matrix_herb=self.map.get_pop_matrix_herb(),
                                           pop_matrix_carn=self.map.get_pop_matrix_carn(),
                                           img_base=self.img_base, img_fmt=self.img_fmt)
        if self.plot_bool:
            self.visualize.draw_layout(self.final_year)

        if self.plot_bool:
            if self.img_years is None:
                self.img_years = self.vis_years

            if self.img_years % self.vis_years != 0:
                raise ValueError('img_years must be multiple of vis_years')

        self.last_year += num_years
        self.final_year = self.year_num + num_years

        if self.plot_bool:
            self.visualize.draw_layout(self.final_year)

        while self.year_num <= self.final_year:
            self.map.yearly_cycle()
            if self.plot_bool and self.year_num % self.vis_years == 0:

                self.visualize.update_plot(pop_herb=self.map.get_pop_tot_num_herb(),
                                           pop_carn=self.map.get_pop_tot_num_carn(),
                                           current_year=self.year_num,
                                           pop_matrix_herb=self.map.get_pop_matrix_herb(),
                                           pop_matrix_carn=self.map.get_pop_matrix_carn(),
                                           weight_list=self.weight_animals_per_species(),
                                           age_list=self.age_animals_per_species(),
                                           fitness_list=self.fitness_animals_per_species())

                if self.img_base is not None:
                    if self.year_num % self.img_years == 0:
                        self.visualize.save_graphics(self.year_num)

            self.year_num += 1

    def add_population(self, population):
        """
        Add a population to the island

        Parameters
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

    def make_movie(self, movie_fmt=None):
        """Create MPEG4 movie from visualization images saved.
            .. :note:
            Requires ffmpeg for MP4 and magick for GIF

            The movie is stored as img_base + movie_fmt
        """

        if self.img_base is None:
            raise RuntimeError("No filename defined.")

        if movie_fmt is None:
            movie_fmt = _DEFAULT_MOVIE_FORMAT

        if movie_fmt == 'mp4':
            try:
                # Parameters chosen according to http://trac.ffmpeg.org/wiki/Encode/H.264,
                # section "Compatibility"
                subprocess.check_call([_FFMPEG_BINARY,
                                       '-i', '{}_%05d.png'.format(self.img_base),
                                       '-y',
                                       '-profile:v', 'baseline',
                                       '-level', '3.0',
                                       '-pix_fmt', 'yuv420p',
                                       '{}.{}'.format(self.img_base, movie_fmt)])
            except subprocess.CalledProcessError as err:
                raise RuntimeError('ERROR: ffmpeg failed with: {}'.format(err))
        elif movie_fmt == 'gif':
            try:
                subprocess.check_call([_MAGICK_BINARY,
                                       '-delay', '1',
                                       '-loop', '0',
                                       '{}_*.png'.format(self.img_base),
                                       '{}.{}'.format(self.img_base, movie_fmt)])
            except subprocess.CalledProcessError as err:
                raise RuntimeError('ERROR: convert failed with: {}'.format(err))
        else:
            raise ValueError('Unknown movie format: ' + movie_fmt)

    def remove_files(self):

        fbase = self.img_base
        img_fmt = self.img_fmt
        for f in glob.glob(f"{fbase}_0*." + str(img_fmt)):
            os.remove(f)
        for f in glob.glob(f"{fbase}*.mp4"):
            os.remove(f)
