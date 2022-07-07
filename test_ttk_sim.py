import random

import ttk_sim
import example_weapons

# Because we are using seeded random values, the order of the tests matters

random.seed(1)
ttk_sim.headshot_chance = 60
ttk_sim.bodyshot_chance = 30

def almost_equal(test, actual):
    return abs(test - actual) < 0.01

def check_ttk(weapon, expected_ttks):
    for expected_ttk in expected_ttks:
        test_ttk = ttk_sim.gunfight(weapon)
        assert almost_equal(test_ttk, expected_ttk)

def test_sturm():
    check_ttk(example_weapons.sturm, [1.5, 0.5, 0, 0, 1.5])

def test_drang():
    check_ttk(example_weapons.drang, [1.2, 1.0, 1.0, 0.6, 0.8])

def test_pom():
    ttks = [1.666, 1.466, 1.733, 0.0666, 2.066]
    check_ttk(example_weapons.piece_of_mind, ttks)

def test_dmt():
    ttks = [1.0, 0.5, 0, 1.0, 0]
    check_ttk(example_weapons.dmt, ttks)

def test_crimson():
    ttks = [1.933, 1.299,1.399,1.733,1.299]
    check_ttk(example_weapons.crimson, ttks)





if __name__ == "__main__":
    test_sturm()
    test_drang()
    test_pom()
    test_dmt()
    test_crimson()