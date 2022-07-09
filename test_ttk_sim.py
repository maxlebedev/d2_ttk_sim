import random
import yaml
from types import SimpleNamespace

import ttk_sim
import example_weapons as ew

ttk_sim.headshot_chance = 60
ttk_sim.bodyshot_chance = 30

def load_test_data():
    with open('expected_ttks.yaml', 'r') as tests:
        return SimpleNamespace(**yaml.safe_load(tests))

td = load_test_data()

def almost_equal(test, actual):
    return abs(test - actual) < 0.01

def check_ttk(weapon, expected_ttks):
    for expected_ttk in expected_ttks:
        test_ttk = ttk_sim.gunfight(weapon)
        assert almost_equal(test_ttk, expected_ttk)

def test_sturm():
    random.seed(1)
    check_ttk(ew.sturm, td.sturm)

def test_drang():
    random.seed(1)
    check_ttk(ew.drang, td.drang)

def test_pom():
    random.seed(1)
    check_ttk(ew.piece_of_mind, td.piece_of_mind)

def test_dmt():
    random.seed(1)
    check_ttk(ew.dmt, td.dmt)

def test_crimson():
    random.seed(1)
    check_ttk(ew.crimson, td.crimson)

def generate_test():
    for weapon in [ew.piece_of_mind, ew.sturm, ew.drang, ew.dmt, ew.crimson]:
        random.seed(1)
        pt = []
        for _ in range(40):
            ttk = ttk_sim.gunfight(weapon)
            pt.append(round(ttk, 2))
        print(f"{weapon.name}: {pt}")

if __name__ == "__main__":
    # gen_ttks = lambda x: [round(ttk_sim.gunfight(x), 2) for _ in range(14)]
    test_sturm()
    test_drang()
    test_pom()
    test_dmt()
    test_crimson()