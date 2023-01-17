
__author__ = "Navneet Sharma and Sushant Kumar Srivastava"
__email__ = "navneet.sharma@nmbu.no and sushant.kumar.sirvastava@nmbu.no"

import pytest
from biosim.simulation import BioSim
from biosim.map import Map
import textwrap


import pytest
from src.biosim.simulation import BioSim
from src.biosim.map import Map


@pytest.mark.parametrize("age, weight", [(10, 20), (30, 50), (20, 50)])
class TestMap():

    @pytest.fixture()
    def island_maps(self):

        return """WWW\nWLW\nWWW"""

    @pytest.mark.parametrize("age, weight", [(10, 20)])
    def create_map_for_test(self, age, weight):
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

        seed = 123213
        t_sim = BioSim(geogr, ini_herbs, seed)
        loc = (1, 1)

        return t_sim, loc
    @pytest.fixture()
    def multiple_island_maps(self):

        return ["LWWW\nWLW\nWWWL","LWWWW\nWWLW\nWLWLW","LWWWLW\nWLLWW\nWWWLW"]

    def test_check_string_type(self):

        with pytest.raises(TypeError):
            Map.check_str_type(4)


    def test_check_dict_type(self):
        with pytest.raises(TypeError):
            Map.check_dict_type([3])


    def test_cell_list(self,island_maps):
        self.m=Map(island_maps)
        self.list_of_cells= self.m.geo_list(island_maps)
        assert self.list_of_cells[1][1] is 'L'

    #this method needs to be tested and modified!!!
    def test_invalid_line_lengths(self,multiple_island_maps):

        for island_maps in multiple_island_maps:
            self.m=Map(island_maps)
            island_maps=self.m.geo_list(island_maps)
            if self.m.check_invalid_line_length(island_maps):
                assert ValueError("The Map cannot have invalid row lengths!!")

    #this method needs to be tested and modified!!!
    def test_invalid_boundary(self,multiple_island_maps):

        for island_maps in multiple_island_maps:
            self.m=Map(island_maps)
            island_maps= textwrap.dedent(str(island_maps)).splitlines()
            if self.m.check_invalid_boundary(island_maps):
                assert ValueError("The Map cannot have invalid boundary!!")

    def test_invalid_character(self,island_maps):
        self.m=Map(island_maps)
        with pytest.raises(ValueError):
            self.m.check_invalid_character(island_maps)

    #needs to be tested
    def test_age_weight_stored(self):
        t,loc=self.create_map_for_test()
        h_weight=t.Map.livable_cells_calculate[loc].initial_population['Herbivore'][0].age
        assert h_weight is 20
        h_age=t.Map.livable_cells_calculate[loc].initial_population['Herbivore'][0].weight
        assert h_age is 15


    # def test_get_population_numbers(self):





