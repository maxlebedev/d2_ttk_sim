import ttk_sim
import random

# Because we are using seeded random values, the order of the tests matters

random.seed(1)
ttk_sim.headshot_chance = 60
ttk_sim.bodyshot_chance = 30

def almost_equal(test, actual):
    return abs(test - actual) < 0.01

sturm = ttk_sim.Weapon(
    name="Sturm",
    mid_burst_time_between_shots=0,
    burst_type=1,
    bodyshot_damage=50,
    headshot_damage=91,
    rpm=120,
)

drang = ttk_sim.Weapon(
    name="Drang",
    mid_burst_time_between_shots=0,
    burst_type=1,
    headshot_damage=50.5,
    bodyshot_damage=36.0,
    rpm=300,
)

piece_of_mind = ttk_sim.Weapon(
    name="Piece of Mind",
    mid_burst_time_between_shots=60.0 / 900.0,
    burst_type=3,
    headshot_damage=23.8,
    bodyshot_damage=14,
    rpm=540,
)

dmt = ttk_sim.Weapon(
    name="dmt",
    mid_burst_time_between_shots=60.0 / 900.0,
    burst_type=1,
    headshot_damage=45.5,
    bodyshot_damage=80.5,
    rpm=120,
)

crimson = ttk_sim.Weapon(
    name="crimson",
    mid_burst_time_between_shots=60.0 / 600.0,
    burst_type=3,
    headshot_damage=30.5,
    bodyshot_damage=19,
    rpm=415.385,
)


def check_ttk(weapon, expected_ttks):
    for expected_ttk in expected_ttks:
        test_ttk = ttk_sim.gunfight(weapon)
        assert almost_equal(test_ttk, expected_ttk)

def test_sturm():
    check_ttk(sturm, [1.5, 0.5, 0, 0, 1.5])

def test_drang():
    check_ttk(drang, [1.2, 1.0, 1.0, 0.6, 0.8])

def test_pom():
    ttks = [1.666, 1.466, 1.733, 0.0666, 2.066]
    check_ttk(piece_of_mind, ttks)

def test_dmt():
    ttks = [1.0, 0.5, 0, 1.0, 0]
    check_ttk(dmt, ttks)

def test_crimson():
    ttks = [1.933, 1.299,1.399,1.733,1.299]
    check_ttk(crimson, ttks)





if __name__ == "__main__":
    test_sturm()
    test_drang()
    test_pom()
    test_dmt()
    test_crimson()