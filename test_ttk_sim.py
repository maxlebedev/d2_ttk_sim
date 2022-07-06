import ttk_sim
import random

random.seed(1)

test_weapon1 = ttk_sim.Weapon(
    name="Sturm",
    mid_burst_time_between_shots=0,
    burst_type=1,
    bodyshot_damage=50,
    headshot_damage=91,
    rpm=120,
)

def test_get_ttk(weapon):
    ttk_sim.headshot_chance = 60
    ttk_sim.bodyshot_chance = 30
    test_ttk = ttk_sim.get_ttk(weapon)
    print(test_ttk)


if __name__ == "__main__":
    test_get_ttk(test_weapon1)