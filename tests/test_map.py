__author__ = "Navneet Sharma and Sushant Kumar Srivastava"
__email__ = "navneet.sharma@nmbu.no and sushant.kumar.sirvastava@nmbu.no"

import pytest
from biosim.simulation import BioSim
from biosim.map import Map
import textwrap
import pytest
from src.biosim.simulation import BioSim
from src.biosim.map import Map


def geo_list(island_map):
    cells_list = textwrap.dedent(str(island_map)).splitlines()
    return [list(row.strip()) for row in cells_list]


# @pytest.mark.parametrize("age, weight", [(10, 20), (30, 50), (20, 50)])
# class TestMap():

@pytest.mark.parametrize('map_str', ["""\
           WWWWL
           WLWWW
           WWWWW""", """\
           WWWWW
           DLWWW
           WWWWW""","""\
           LWWWWWWWWWWWW
           WLWWWLLLLLLLL
           WWWWWDDDDDDDD"""])
def test_check_invalid_boundaries(map_str):

    with pytest.raises(ValueError):
        m = Map(map_str)
        # assert err.type is ValueError
@pytest.mark.parametrize('map_str', ["""\
           WWWW
           WLWWW
           WWWWW""", """\
           WWWWW
           WW
           WWWWW""","""\
           WWWWWWWWWWWWWWWWWWWWW
           WLWWW
           WWWWW"""])
def test_check_invalid_line_length(map_str):

    with pytest.raises(ValueError):
        m = Map(map_str)

@pytest.mark.parametrize('map_str', ["""\
           WWWW@
           WLWWW
           WWWWW""", """\
           WWWWW
           D.WWW
           WWWWW""","""\
           LWWWWWWWWWWWW
           WLWWWLL?LLLLL
           WWWWWDDDDDDDD"""])
def test_check_invalid_character(map_str):

    with pytest.raises(ValueError):
        m = Map(map_str)

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


def test_cell_list():
    island_maps="""\
               WWW
               WLW
               WWW"""
    m = Map(island_maps)
    list_of_cells = geo_list(island_maps)
    assert list_of_cells[1][1] is 'L'

def test_age_weight_stored(self):
    t, loc = self.create_map_for_test()
    h_weight = t.Map.livable_cells_calculate[loc].initial_population['Herbivore'][0].age
    assert h_weight is 20
    h_age = t.Map.livable_cells_calculate[loc].initial_population['Herbivore'][0].weight
    assert h_age is 15

# def test_get_population_numbers(self):
