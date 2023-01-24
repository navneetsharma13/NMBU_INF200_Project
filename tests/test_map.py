
"""
This is the Test Map file which tests if all the functions in map.py runs properly with the
Biosim package written for the INF200 project January 2023.
"""

__author__ = "Navneet Sharma and Sushant Kumar Srivastava"
__email__ = "navneet.sharma@nmbu.no and sushant.kumar.srivastava@nmbu.no"

import textwrap
import pytest
from biosim.simulation import BioSim
from biosim.map import Map


class TestMap:

    @staticmethod
    def geo_list(island_map):
        """This method converts island_map str into list with each element corresponding to
        each cell element in the map

        Returns:
        ----------
        List with element as each cell element in map.
        """
        cells_list = textwrap.dedent(str(island_map)).splitlines()
        return [list(row.strip()) for row in cells_list]

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
        a different boundary for island_maps than only 'Water'.
        """
        with pytest.raises(ValueError):
            Map(map_str)

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
            Map(map_str)

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
            Map(map_str)

    # @pytest.fixture(autouse=True)
    def test_cell_list(self):
        """Test if the method 'geo_list()' generates a
        correct list of geographies with the correct coordinates.
        """
        island_maps = """\
                   WWW
                   WLW
                   WWW"""
        Map(island_maps)
        list_of_cells = self.geo_list(island_maps)
        assert list_of_cells[1][1] == 'L'

    @pytest.fixture(autouse=True)
    def create_map_for_test(self, age=10, weight=20):
        """This method generates a basic BioSim class with a given map and
        population and returns the BioSim object and location of animals

        Returns:
        ----------
        tuple
        """
        geogr = """\
                       WWW
                       WLW
                       WWW"""
        geogr = textwrap.dedent(geogr)
        ini_herbs = [
            {
                "loc": (2, 2),
                "pop": [{"species": "Herbivore", "age": age, "weight": weight}],

            }]

        ini_carns = [
            {
                "loc": (2, 2),
                "pop": [{"species": "Carnivore", "age": age, "weight": weight}],

            }]

        seed = 123213
        t_sim = BioSim(geogr, ini_herbs, seed)
        t_sim.add_population(ini_carns)
        loc = (1, 1)

        return t_sim, loc

    def test_age_weight_stored(self, create_map_for_test):
        """Test if the method 'def add_population()' correctly store the age
        and weight on animal_object.
        """
        t_sim, loc = create_map_for_test
        h1_age = t_sim.map.livable_cell_calculate()[loc].initial_population['Herbivore'][0].age
        h1_age_compare = t_sim.map.get_pop_age_herb()[0]
        assert h1_age is h1_age_compare

        h1_weight = t_sim.map.livable_cell_calculate()[loc].initial_population['Herbivore'][
            0].weight
        h1_weight_compare = t_sim.map.get_pop_weight_herb()[0]
        assert h1_weight is h1_weight_compare

        c1_age = t_sim.map.livable_cell_calculate()[loc].initial_population['Carnivore'][0].age
        c1_age_compare = t_sim.map.get_pop_age_carn()[0]
        assert c1_age is c1_age_compare

        c1_weight = t_sim.map.livable_cell_calculate()[loc].initial_population['Carnivore'][
            0].weight
        c1_weight_compare = t_sim.map.get_pop_weight_carn()[0]
        assert c1_weight is c1_weight_compare

    def test_get_population_numbers(self, create_map_for_test):
        """Test if the method 'get_pop_tot_num_herb()' and 'get_pop_tot_num_carn()' correctly
        gets the entire population number by comparing it with get_pop_tot_num.
        """
        t_sim, loc = create_map_for_test
        assert t_sim.map.get_pop_tot_num_herb() + \
               t_sim.map.get_pop_tot_num_carn() == t_sim.map.get_pop_tot_num()

    def test_pop_matrix_herbivore(self, create_map_for_test):
        """Test if the method 'get_pop_matrix_herb()' returns the correct no of herbivore at
        a given coordinate by comparing it with get_pop_tot_num_herb().
        """
        t_sim, loc = create_map_for_test
        assert t_sim.map.get_pop_matrix_herb()[loc[0]][loc[1]] is t_sim.map.get_pop_tot_num_herb()

    def test_pop_matrix_carnivore(self, create_map_for_test):
        """Test if the method 'get_pop_matrix_carn()' returns the correct no of carnivore at
        a given coordinate by comparing it with get_pop_tot_num_carn().
        """
        t_sim, loc = create_map_for_test
        assert t_sim.map.get_pop_matrix_carn()[loc[0]][loc[1]] is t_sim.map.get_pop_tot_num_carn()

    def test_unique_row(self, create_map_for_test):
        """Test if the method unique_row() return correct no of rows.
        """
        t_sim, loc = create_map_for_test
        assert len(set(t_sim.map.calculate_animal_count()['Row_no'])) is len(
            t_sim.map.unique_rows())

    def test_unique_column(self, create_map_for_test):
        """Test if the method unique_row() return correct no of rows.
        """
        t_sim, loc = create_map_for_test
        assert len(set(t_sim.map.calculate_animal_count()['Col_no'])) is len(
            t_sim.map.unique_columns())

    def test_add_population(self, create_map_for_test):
        """Test if the animal count is getting updated after adding population.
        """
        t_sim, loc = create_map_for_test
        pop_before_herb = t_sim.map.get_pop_tot_num_herb()
        ini_herbs_1 = [
            {
                "loc": (2, 2),
                "pop": [{"species": "Herbivore", "age": 24, "weight": 60}],

            }]
        t_sim.add_population(ini_herbs_1)
        pop_after_herb = t_sim.map.get_pop_tot_num_herb()
        assert pop_after_herb is pop_before_herb + 1

        pop_before_carn = t_sim.map.get_pop_tot_num_carn()
        ini_carns_1 = [
            {
                "loc": (2, 2),
                "pop": [{"species": "Carnivore", "age": 31, "weight": 50}],

            }]
        t_sim.add_population(ini_carns_1)
        pop_after_carn = t_sim.map.get_pop_tot_num_carn()
        assert pop_after_carn is pop_before_carn + 1

    def test_create_neighbours(self, create_map_for_test):
        """Test if the correct no of neighbours are getting created for a given location.
        """
        t_sim, loc = create_map_for_test
        len_neighbours_at_loc_01 = len(t_sim.map.create_neighbours_dict()[loc[0] - 1, loc[0]])
        assert len_neighbours_at_loc_01 == 3
