import random

import ttk_sim
import example_weapons

# Because we are using seeded random values, the order of the tests matters
# To add one more test to a weapon, populate the next ttk value, and recompute all following tests

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
    ttks = [1.5, 0.5, 0.0, 0.0, 1.5, 2.0, 0.0, 1.5, 1.5, 1.0, 1.0, 1.5, 2.0, 0.5]
    check_ttk(example_weapons.sturm, ttks)

def test_drang():
    ttks = [0.0, 1.0, 1.0, 0.8, 0.0, 0.8, 0.2, 0.0, 0.8, 0.8, 0.4, 1.0, 1.0, 1.2]
    check_ttk(example_weapons.drang, ttks)

def test_pom():
    ttks = [0.33, 0.13, 1.4, 0.0, 0.4, 1.0, 1.33, 1.4, 1.4, 1.4, 2.07, 1.33, 0.67, 1.33]
    check_ttk(example_weapons.piece_of_mind, ttks)

def test_dmt():
    ttks = [1.0, 0.5, 1.0, 1.0, 1.5, 0.5, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 2.0, 1.0]
    check_ttk(example_weapons.dmt, ttks)

def test_crimson():
    ttks = [1.3, 1.3, 1.3, 1.3, 1.3, 1.07, 0.0, 0.43, 1.4, 0.53, 0.87, 1.3, 1.5, 1.3]
    check_ttk(example_weapons.crimson, ttks)

if __name__ == "__main__":
    # gen_ttks = lambda x: [round(ttk_sim.gunfight(x), 2) for _ in range(14)]
    test_sturm()
    test_drang()
    test_pom()
    test_dmt()
    test_crimson()