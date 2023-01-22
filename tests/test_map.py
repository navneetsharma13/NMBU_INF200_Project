__author__ = "Navneet Sharma and Sushant Kumar Srivastava"
__email__ = "navneet.sharma@nmbu.no and sushant.kumar.srivastava@nmbu.no"

import random

import pytest
from biosim.simulation import BioSim
from biosim.map import Map
import textwrap
import pytest
from src.biosim.simulation import BioSim
from src.biosim.map import Map
from src.biosim.fauna import Herbivore, Carnivore
from src.biosim.landscape import Landscape


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
           WWWWW""", """\
           LWWWWWWWWWWWW
           WLWWWLLLLLLLL
           WWWWWDDDDDDDD"""])
def test_check_invalid_boundaries(map_str):
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
def test_check_invalid_line_length(map_str):
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
def test_check_invalid_character(map_str):
    with pytest.raises(ValueError):
        Map(map_str)


@pytest.fixture(autouse=True)
def test_cell_list():
    island_maps = """\
               WWW
               WLW
               WWW"""
    Map(island_maps)
    list_of_cells = geo_list(island_maps)
    assert list_of_cells[1][1] is 'L'


@pytest.fixture(autouse=True)
def create_map_for_test(age=10, weight=20):
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


def test_age_weight_stored(create_map_for_test):
    t_sim, loc = create_map_for_test
    h1_age = t_sim.map.livable_cell_calculate()[loc].initial_population['Herbivore'][0].age
    h1_age_compare = t_sim.map.get_pop_age_herb()[0]
    assert h1_age is h1_age_compare

    h1_weight = t_sim.map.livable_cell_calculate()[loc].initial_population['Herbivore'][0].weight
    h1_weight_compare = t_sim.map.get_pop_weight_herb()[0]
    assert h1_weight is h1_weight_compare

    c1_age = t_sim.map.livable_cell_calculate()[loc].initial_population['Carnivore'][0].age
    c1_age_compare = t_sim.map.get_pop_age_carn()[0]
    assert c1_age is c1_age_compare

    c1_weight = t_sim.map.livable_cell_calculate()[loc].initial_population['Carnivore'][0].weight
    c1_weight_compare = t_sim.map.get_pop_weight_carn()[0]
    assert c1_weight is c1_weight_compare


def test_get_population_numbers(create_map_for_test):
    t_sim, loc = create_map_for_test

    assert t_sim.map.get_pop_tot_num_herb() + \
           t_sim.map.get_pop_tot_num_carn() == t_sim.map.get_pop_tot_num()


def test_pop_matrix_herbivore(create_map_for_test):
    t_sim, loc = create_map_for_test
    assert t_sim.map.get_pop_matrix_herb()[loc[0]][loc[1]] is t_sim.map.get_pop_tot_num_herb()


def test_pop_matrix_carnivore(create_map_for_test):
    t_sim, loc = create_map_for_test
    assert t_sim.map.get_pop_matrix_carn()[loc[0]][loc[1]] is t_sim.map.get_pop_tot_num_carn()


def test_unique_row(create_map_for_test):
    t_sim, loc = create_map_for_test
    assert len(set(t_sim.map.calculate_animal_count()['Row_no'])) is len(t_sim.map.unique_rows())


def test_unique_column(create_map_for_test):
    t_sim, loc = create_map_for_test
    assert len(set(t_sim.map.calculate_animal_count()['Col_no'])) is len(t_sim.map.unique_columns())


def test_add_population(create_map_for_test):

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


def test_create_neighbours(create_map_for_test):
    t_sim, loc = create_map_for_test
    len_neighbours_at_loc_01 = len(t_sim.map.create_neighbours_dict()[loc[0] - 1, loc[0]])
    assert len_neighbours_at_loc_01 is 1


def test_migrate_cell_calculate(create_map_for_test):
    t_sim, loc = create_map_for_test
    location_migration_cells = t_sim.map.migrate_cell_calculate().keys()
    assert list(location_migration_cells) == [loc]
