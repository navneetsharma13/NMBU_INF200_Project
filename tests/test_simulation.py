import pytest

from biosim.simulation import BioSim

# Should add fixture to remove generated image and movie files.

class TestSimulation:
    def test_empty_island(self):
        "Empty island can be created"
        BioSim(island_map="WW\nWW", ini_pop=[], seed=1)

    def test_minimal_island(self):
        "Island of single jungle cell can be created"
        BioSim(island_map="WWW\nWLW\nWWW", ini_pop=[], seed=1)

    def test_all_landscape_types(self):
        "All types of Landscapes can be created"
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
    def test_check_invalid_boundaries(self,map_str):
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
    def test_check_invalid_line_length(self,map_str):
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
    def test_check_invalid_character(self,map_str):
        with pytest.raises(ValueError):
            BioSim(island_map=map_str, ini_pop=[], seed=1)


    @pytest.fixture
    def basic_sim(self):
        """Return a simple island for used in various tests below"""
        return BioSim(island_map="WWWW\nWHLW\nWWWW", ini_pop=[], seed=1)

    def test_simulate(self,basic_sim):
        basic_sim.simulate(num_years=10)

    def test_add_population(self,basic_sim):
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
    def test_get_years(self,basic_sim):

        self.test_add_population(basic_sim)
        basic_sim.simulate(num_years=2)
        assert basic_sim.year == 2

    def test_get_total_fauna(self,basic_sim):
        assert basic_sim.num_animals == 0

    def test_get_fauna_by_species(self,basic_sim):
        assert basic_sim.num_animals_per_species=={"Herbivore": 0,
            "Carnivore": 0}
    def test_fauna_distribution(self,basic_sim):

        self.test_add_population(basic_sim)

        herb_matrix=basic_sim.map.get_pop_matrix_herb()
        carn_matrix=basic_sim.map.get_pop_matrix_carn()

        assert herb_matrix[1-1][2-1] is 1
        assert herb_matrix[1-1][3-1] is 1

        assert carn_matrix[1-1][2-1] is 1
        assert carn_matrix[1-1][3-1] is 1

    def test_set_fig_limit(self):

         BioSim(
            island_map="WWWW\nWHLW\nWWWW",
            ini_pop=[],
            seed=1,
            ymax_animals=20,
            cmax_animals={"Herbivore": 10, "Carnivore": 20},
        )
    def test_multi_simulate(self,basic_sim):
        basic_sim.simulate(num_years=10)
        basic_sim.simulate(num_years=10)


