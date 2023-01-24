
"""
This is the Test Simulation file which tests if all the functions in simulation.py runs properly
with the Biosim package written for the INF200 project January 2023.
"""

__author__ = "Navneet Sharma and Sushant Kumar Srivastava"
__email__ = "navneet.sharma@nmbu.no and sushant.kumar.srivastava@nmbu.no"

import pytest

from biosim.simulation import BioSim


class TestSimulation:
    def test_empty_island(self):
        """Empty island can be created
        """
        BioSim(island_map="WW\nWW", ini_pop=[], seed=1)

    def test_minimal_island(self):
        """Island of single jungle cell can be created
        """
        BioSim(island_map="WWW\nWLW\nWWW", ini_pop=[], seed=1)

    def test_all_landscape_types(self):
        """All types of Landscapes can be created
        """
        BioSim(island_map="WWWW\nWLDW\nWHLW\nWWWW", ini_pop=[], seed=1)

    @pytest.mark.parametrize('map_str', ["""\
                   WWWWL
                   WLWWW
                   WWWWW""", """\
                   WWWWW
                   DLWWW
                   WWWWW""", """\
                   LWWWWWWWWWWWW
                   WLWWWLLLLLLLL
                   WWWWWDDDDDDDD"""])
    def test_check_invalid_boundaries(self, map_str):
        """Test if the method 'check_invalid_maps()' identifies
        a different boundary for island_maps than only 'Water'"""
        with pytest.raises(ValueError):
            BioSim(island_map=map_str, ini_pop=[], seed=1)

    @pytest.mark.parametrize('map_str', ["""\
                   WWWW
                   WLWWW
                   WWWWW""", """\
                   WWWWW
                   WW
                   WWWWW""", """\
                   WWWWWWWWWWWWWWWWWWWWW
                   WLWWW
                   WWWWW"""])
    def test_check_invalid_line_length(self, map_str):
        """Test if the method 'check_invalid_maps()' identifies
        a different line length for island_maps.
        """
        with pytest.raises(ValueError):
            BioSim(island_map=map_str, ini_pop=[], seed=1)

    @pytest.mark.parametrize('map_str', ["""\
                   WWWW@
                   WLWWW
                   WWWWW""", """\
                   WWWWW
                   D.WWW
                   WWWWW""", """\
                   LWWWWWWWWWWWW
                   WLWWWLL?LLLLL
                   WWWWWDDDDDDDD"""])
    def test_check_invalid_character(self, map_str):
        """Test if the method 'check_invalid_maps()' identifies
        an invalid character for island_maps other than landscape cells.
        """
        with pytest.raises(ValueError):
            BioSim(island_map=map_str, ini_pop=[], seed=1)

    @pytest.fixture
    def basic_sim(self):
        """Return a simple island for used in various tests below"""
        return BioSim(island_map="WWWW\nWHLW\nWWWW", ini_pop=[], seed=1, vis_years=0)

    def test_simulate(self, basic_sim):
        """Test that simulation can be called with visualization step values.
        """
        basic_sim.simulate(num_years=10)

    def test_add_population(self, basic_sim):
        """Test if the method add_population() is working correctly.
        """
        basic_sim.add_population([
            {
                "loc": (1, 2),
                "pop": [
                    {"species": "Herbivore", "age": 10, "weight": 20.0},
                    {"species": "Carnivore", "age": 30, "weight": 40.0},
                ],
            },
            {
                "loc": (1, 3),
                "pop": [
                    {"species": "Herbivore", "age": 10, "weight": 20.0},
                    {"species": "Carnivore", "age": 30, "weight": 40.0},
                ],
            },
        ])

    def test_get_years(self, basic_sim):
        """Test that number of years simulated is available.
        """
        self.test_add_population(basic_sim)
        basic_sim.simulate(num_years=2)
        assert basic_sim.year == 2

    def test_get_total_fauna(self, basic_sim):
        """Test that total number of animals is available.
        """
        assert basic_sim.num_animals == 0

    def test_get_fauna_by_species(self, basic_sim):
        """Test that total number of animals per species is available.
        """
        assert basic_sim.num_animals_per_species == {"Herbivore": 0,
                                                     "Carnivore": 0}

    def test_fauna_distribution(self, basic_sim):
        """Test that animal distribution is correctly updated at locations after adding
        population.
        """
        self.test_add_population(basic_sim)

        herb_matrix = basic_sim.map.get_pop_matrix_herb()
        carn_matrix = basic_sim.map.get_pop_matrix_carn()

        assert herb_matrix[1 - 1][2 - 1] == 1
        assert herb_matrix[1 - 1][3 - 1] == 1

        assert carn_matrix[1 - 1][2 - 1] == 1
        assert carn_matrix[1 - 1][3 - 1] == 1

    def test_set_fig_limit(self):
        """Test that y-axis and color limits for plots can be set.
        """
        BioSim(
            island_map="WWWW\nWHLW\nWWWW",
            ini_pop=[],
            seed=1,
            ymax_animals=20,
            cmax_animals={"Herbivore": 10, "Carnivore": 20},
        )

    def test_multi_simulate(self, basic_sim):
        """Test that simulation can be called repeatedly
        """
        basic_sim.simulate(num_years=10)
        basic_sim.simulate(num_years=10)
