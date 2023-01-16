from src.biosim.simulation import BioSim

# Should add fixture to remove generated image and movie files.


def test_sim():
    sim = BioSim((3, 5), 0.1, seed=12345)
    sim.simulate(5, 1, 5)
    sim.make_movie()
