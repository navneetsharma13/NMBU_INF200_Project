"""
This is the geography pytest package which is a test package for the  BioSim packages written for
 the INF200 project January 2023.
"""

__author__ = "Navneet Sharma and Sushant Kumar Srivastava"
__email__ = "navneet.sharma@nmbu.no and sushant.kumar.srivastava@nmbu.no"

import random
import textwrap
import pytest
from biosim.landscape import Lowland, Highland, Desert
from biosim.simulation import BioSim


def test_verify_unknown_parameters():
    """Test method 'verify_parameters()' if it does not identify the given parameter as incorrect
     and return ValueError"""
    with pytest.raises(ValueError):
        Lowland.verify_parameters(params={'f_min': 100})
        Highland.verify_parameters(params={'f_min': 100})


def test_verify_known_parameters():
    """Test method 'verify_parameters()' if it does not identify the given parameter are correct and
     returns ValueError"""
    Lowland.verify_parameters(params={'f_max': 100})
    Highland.verify_parameters(params={'f_max': 100})


def test_negative_parameters():
    """Test method 'verify_non_valid_parameters(param_key, params)' if it identifies the
    negative value of a given parameter and returns ValueError"""
    param_key, params = 'f_max', {'f_max': -344}
    with pytest.raises(ValueError):
        Lowland.verify_non_valid_parameters(param_key, params)
        Highland.verify_non_valid_parameters(param_key, params)


def test_string_parameters():
    """Test method 'verify_non_valid_parameters(param_key, params)' if it identifies the
    negative value of a given parameter and returns ValueError"""
    param_key, params = 'f_max', {'f_max': "text"}
    with pytest.raises(ValueError):
        Lowland.verify_non_valid_parameters(param_key, params)
        Highland.verify_non_valid_parameters(param_key, params)


@pytest.mark.parametrize("age, weight", [(5, 40), (10, 20), (30, 50), (20, 50)])
class TestLandscape:

    @pytest.mark.parametrize("age, weight", [(5, 40), (10, 20), (30, 50), (20, 50)])
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

    def test_fauna_aging(self, age, weight):
        """Test if the method 'age_increase()' correctly increases in 1 year all
            the animal_objects stored in a specific geo_object"""

        t_sim, loc = self.create_map_for_test(age, weight)
        loc_object = t_sim.map.livable_cell_calculate()[loc]
        for _ in range(len(loc_object.initial_population['Herbivore'])):
            herb_object = loc_object.initial_population['Herbivore'][_]
            herb_age_before = herb_object.age
            loc_object.age_increase()
            herb_age_after = herb_object.age
            assert herb_age_after is (herb_age_before + 1)

    def test_herbivore_feeding(self, age, weight):
        """This test method verifies different cases for the feed_herbivore():
            a.) To check if the fodder reduces when an animal eats it.
            b.) To check if the weight of the animal increases after eat.
            c.) To check if the fitness of the animal gets updated after feeding is done.
        """
        t_sim, loc = self.create_map_for_test(age, weight)
        loc_object = t_sim.map.livable_cell_calculate()[loc]
        old_fodder = loc_object.fodder
        herb_object = loc_object.initial_population['Herbivore'][0]
        old_herb_weight = herb_object.weight
        old_herb_fitness = herb_object.fitness
        loc_object.feed_herbivore()
        updated_fodder = loc_object.fodder
        updated_herb_weight = herb_object.weight
        updated_herb_fitness = herb_object.fitness

        assert old_fodder > updated_fodder
        assert old_herb_weight < updated_herb_weight
        assert old_herb_fitness != updated_herb_fitness

    def test_carnivore_feeding(self, age, weight, mocker):
        mocker.patch('random.random', return_value=0.00115)

        """This test method verifies different cases for the feed_herbivore():
            a.) To check if the fodder reduces when an animal eats it.
            b.) To check if the weight of the animal increases after eat.
            c.) To check if the fitness of the animal gets updated after feeding is done.
        """
        ini_carns = [
            {
                "loc": (2, 2),
                "pop": [
                    {"species": "Carnivore", "age": 15, "weight": 40}
                    for _ in range(40)],
            }]
        t_sim, loc = self.create_map_for_test(age, weight)
        loc_object = t_sim.map.livable_cell_calculate()[loc]
        t_sim.add_population(ini_carns)
        carn_object = loc_object.initial_population['Carnivore'][0]
        old_carn_weight = carn_object.weight
        loc_object.feed_carnivore()
        updated_carn_weight = carn_object.weight
        assert old_carn_weight < updated_carn_weight

    def test_fauna_death(self, age, weight, mocker):
        mocker.patch('random.random', return_value=0.00001)

        """This test method verifies different cases for the feed_herbivore():
            a.) To check if the fodder reduces when an animal eats it.
            b.) To check if the weight of the animal increases after eat.
            c.) To check if the fitness of the animal gets updated after feeding is done.
        """
        ini_carns = [
            {
                "loc": (2, 2),
                "pop": [
                    {"species": "Carnivore", "age": 15, "weight": 40}
                    for _ in range(40)],
            }]
        ini_herbs = [
            {
                "loc": (1, 1),
                "pop": [
                    {"species": "Herbivore", "age": 5,
                     "weight": random.randint(1, 5)}
                    for _ in range(150)
                ],
            }
        ]
        t_sim, loc = self.create_map_for_test(age, weight)
        loc_object = t_sim.map.livable_cell_calculate()[loc]
        t_sim.add_population(ini_carns)
        t_sim.add_population(ini_herbs)
        loc_object.animal_die()
        assert len(loc_object.initial_population["Carnivore"]) < 40
        assert len(loc_object.initial_population["Herbivore"]) < 151

    def test_fauna_weight_loss(self, age, weight):
        """Test if the method 'age_increase()' correctly increases in 1 year all
            the animal_objects stored in a specific geo_object

        Parameters
        ----------
        weight : object"""
        ini_herbs = [
            {
                "loc": (2, 2),
                "pop": [
                    {"species": "Herbivore", "age": 5, "weight": 40}
                    for _ in range(150)
                ],
            }
        ]
        t_sim, loc = self.create_map_for_test(age, weight)
        t_sim.add_population(ini_herbs)
        loc_object = t_sim.map.livable_cell_calculate()[loc]
        for _ in range(len(loc_object.initial_population['Herbivore'])):
            herb_object = loc_object.initial_population['Herbivore'][_]
            herb_weight_before = herb_object.weight
            loc_object.weight_decrease()
            herb_weight_after = herb_object.weight
            assert herb_weight_after < herb_weight_before


def test_fauna_count_after_birth():
    """This test that the number of animals in the cell increases after birth or not.
    """
    geogr = """\
                       WWW
                       WLW
                       WWW"""
    geogr = textwrap.dedent(geogr)

    ini_herbs = [
        {
            "loc": (2, 2),
            "pop": [
                {"species": "Herbivore", "age": 5, "weight": 40}
                for _ in range(150)
            ],
        }
    ]

    seed = 23423
    t_sim = BioSim(geogr, ini_herbs, seed)
    fauna_count_before = t_sim.num_animals
    loc = (1, 1)
    loc_object = t_sim.map.livable_cell_calculate()[loc]
    loc_object.add_newborn()
    assert fauna_count_before - t_sim.num_animals < 0


def test_fauna_weight_after_birth():
    """This test that the number of animals in the cell increases after birth or not.
    """
    geogr = """\
                       WWW
                       WLW
                       WWW"""
    geogr = textwrap.dedent(geogr)

    ini_herbs = [
        {
            "loc": (2, 2),
            "pop": [
                {"species": "Herbivore", "age": 5, "weight": 40}
                for _ in range(150)
            ],
        }
    ]

    seed = 23423
    t_sim = BioSim(geogr, ini_herbs, seed)
    loc = (1, 1)
    loc_object = t_sim.map.livable_cell_calculate()[loc]
    fauna_weight_before = 0
    for _ in range(len(loc_object.initial_population['Herbivore'])):
        herb_object = loc_object.initial_population['Herbivore'][_]
        fauna_weight_before += herb_object.weight
    loc_object.add_newborn()
    fauna_weight_after = 0
    for _ in range(len(loc_object.initial_population['Herbivore'])):
        herb_object = loc_object.initial_population['Herbivore'][_]
        fauna_weight_after += herb_object.weight

    assert fauna_weight_after < fauna_weight_before


@pytest.mark.parametrize("age, weight", [(5, 40), (10, 20), (30, 50), (20, 50)])
def test_migration(age, weight):
    """This tests the migration method checking if the animals have
    moved to the all 4th neighbour cells."""

    geogr = """\
                       WWWWW
                       WLLLW
                       WHLLW
                       WDDDW
                       WWWWW"""
    geogr = textwrap.dedent(geogr)
    ini_herbs = [
        {
            "loc": (3, 3),
            "pop": [{"species": "Herbivore", "age": age, "weight": weight}
                    for _ in range(150)
                    ],
        }]

    seed = 123213
    t_sim = BioSim(geogr, ini_herbs, seed)
    loc = (2, 2)
    loc_object = t_sim.map.livable_cell_calculate()[loc]
    neighbours = t_sim.map.neighbours_dict[(2, 2)]
    top_neighbour = neighbours[1]
    bottom_neighbour = neighbours[2]
    left_neighbour = neighbours[0]
    right_neighbour = neighbours[3]
    assert type(top_neighbour) == Lowland
    assert type(bottom_neighbour) == Desert
    assert type(left_neighbour) == Highland
    assert type(right_neighbour) == Lowland

    loc_object.animal_migrate(neighbours)
    top_neighbour_pop = t_sim.map.get_pop_matrix_herb()[1][2]
    bottom_neighbour_pop = t_sim.map.get_pop_matrix_herb()[3][2]
    left_neighbour_pop = t_sim.map.get_pop_matrix_herb()[2][1]
    right_neighbour_pop = t_sim.map.get_pop_matrix_herb()[2][3]
    assert top_neighbour_pop != 0
    assert bottom_neighbour_pop != 0
    assert left_neighbour_pop != 0
    assert right_neighbour_pop != 0

class TestHighland:

    @pytest.fixture
    def highland_cell(self):
        """Create basic Highland instance for testing"""
        return Highland()

    def test_highland_fmax(self, highland_cell):
        """
        :property: Highland.params
        Test that highland parameters are correct
        """
        assert highland_cell.params['f_max'] == 300.0

    def test_highland_mainland(self, highland_cell):
        """
        :property: Highland.params
        Test that is_mainland property is True
        """
        assert highland_cell.is_mainland

    def test_highland_fodder(self, highland_cell):
        """
        :cls property: Highland._fodder
        Fodder attribute of instance can be accessed and has the right value
        """
        assert highland_cell._fodder == highland_cell.params['f_max']

    def test_fodder_setter(self, highland_cell):
        """
        :setter: LandscapeCell.fodder
        :property: Highland._fodder
        Fodder attribute of instance can be accessed and has the right value
        """
        highland_cell.fodder = 200.0
        assert highland_cell._fodder == 200.0

    def test_reset_animals(self, highland_cell):
        """
        :method: LandscapeCell.add_animal
        :method: LandscapeCell.reset_animals
        :property: LandscapeCell.carnivores
        :property: LandscapeCell.has_moved
        Test that has_moved property is correctly set and reset
        """
        highland_cell.add_animals([Carnivore(), Herbivore()])
        if highland_cell.carnivores[0].has_moved:
            highland_cell.reset_animals()
        assert not highland_cell.carnivores[0].has_moved

    def test_shuffle_herbs(self, highland_cell):
        """
        :method: LandscapeCell.add_animals
        :method: LandscapeCell.randomize_herbs
        Test that shuffle method shuffles herbivores list
        """
        highland_cell.add_animals([Herbivore() for _ in range(1000)])
        original_herbs = [animal for animal in highland_cell.herbivores]
        highland_cell.randomize_herbs()
        assert highland_cell.herbivores != original_herbs

    def test_repr_and_str(self, highland_cell):
        """
        Test __repr__ and __str__ dunder methods for Highland cell
        """
        assert repr(highland_cell) == str(highland_cell) == 'Highland(f_max: 300.0)'

    def test_set_params(self, highland_cell):
        """
        :cls method: Highland.set_params
        Test that error is raised when invalid key is passed
        """
        with pytest.raises(AttributeError):
            highland_cell.set_params({'ff_maxx': 200.0})

    def test_add_remove_animals(self, highland_cell):
        """
        :method: LandscapeCell.add_animals
        :method: LandscapeCell.remove_animals
        :property: LandscapeCell.animal_count
        Test that animals can be added and removed correctly
        """
        animals = [Herbivore(), Carnivore(), Herbivore()]
        highland_cell.add_animals(animals)
        highland_cell.remove_animals([animals[0], animals[1]])
        assert highland_cell.herb_count == 1

    @pytest.mark.parametrize('add_remove_func',
                             ['add', 'remove'])
    def test_invalid_add_remove_animals(self, highland_cell, add_remove_func):
        """
        :method: LandscapeCell.add_animals
        :method: LandscapeCell.remove_animals
        Test that error is raised when non-instance objects are passed to methods
        """
        with pytest.raises(ValueError):
            if add_remove_func == 'add':
                highland_cell.add_animals(['Herbivore'])
            else:
                highland_cell.remove_animals(['Carnivore'])

    def test_sorted_herbivores_and_carnivores(self, highland_cell):
        """
        :method: LandscapeCell.add_animals
        :method: LandscapeCell.sorted_herbivores
        :method: LandscapeCell.sorted_carnivores
        Check that sorting algorithms sort the lists by fitness
        """
        highland_cell.add_animals([Herbivore(weight=50), Herbivore(weight=20)])
        highland_cell.add_animals([Carnivore(weight=25), Carnivore(weight=40)])
        sorted_herbivores = list([herb[0] for herb in highland_cell.sorted_herbivores])
        sorted_carnivores = highland_cell.sorted_carnivores

        assert sorted_herbivores == highland_cell.herbivores[::-1]
        assert sorted_carnivores == highland_cell.carnivores[::-1]

    def test_is_empty(self, highland_cell):
        """
        :setter: LandscapeCell.fodder
        :property: LandscapeCell.is_empty
        """
        highland_cell.fodder = 0
        assert highland_cell.is_empty


class TestLowland:
    @pytest.fixture
    def lowland_cell(self):
        """Create basic Lowland instance"""
        return Lowland()

    def test_lowland_fmax(self, lowland_cell):
        """
        :cls property: Lowland.params
        Check that f_max is correct
        """
        assert lowland_cell.params['f_max'] == 800.0

    def test_lowland_mainland(self, lowland_cell):
        """
        :property: LandscapeCell.is_mainland
        Check that is_mainland returns True
        """
        assert lowland_cell.is_mainland

    def test_lowland_fodder(self, lowland_cell):
        """
        :property: LandscapeCell.fodder
        Fodder attribute of instance can be accessed and has the right value
        """
        assert lowland_cell.fodder == lowland_cell.params['f_max']


class TestDesert:
    @pytest.fixture
    def desert_cell(self):
        """Create basic desert instance"""
        return Desert()

    def test_desert_fmax(self, desert_cell):
        """
        :cls property: Desert.params
        Test that class parameters are correct
        """
        assert desert_cell.params['f_max'] == 0.0

    def test_desert_mainland(self, desert_cell):
        """
        :property: LandscapeCell.is_mainland
        Test that is_mainland returns True
        """
        assert desert_cell.is_mainland

    def test_desert_fodder(self, desert_cell):
        """
        :property: LandscapeCell._fodder
        Fodder attribute of instance can be accessed and has the right value
        """
        assert desert_cell._fodder == desert_cell.params['f_max']


class TestWater:

    def test_water_instance(self):
        """
        :cls property: Water.is_mainland
        Test that is_mainland returns False
        """
        water = Water()
        assert not water.is_mainland

    def test_repr_and_str_water(self):
        """
        :method: Water.__repr__
        :method: Water.__str__
        Test that dunder methods return correct value
        """
        water = Water()
        assert repr(water) == str(water) == 'Water cell'


