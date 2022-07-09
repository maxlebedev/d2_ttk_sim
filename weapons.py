from dataclasses import dataclass

import ttk_sim

@dataclass
class Weapon:
    name: str = ""
    mid_burst_time_between_shots: float = 0.0
    burst_type: int = 0
    rpm: float = 0.0
    headshot_damage: float = 0.0
    bodyshot_damage: float = 0.0

    def get_time_between_shots(self):
        time_between_bursts = (self.burst_type - 1) * self.mid_burst_time_between_shots
        return 60.0 * self.burst_type / self.rpm - time_between_bursts

sturm = Weapon(
    name="sturm",
    mid_burst_time_between_shots=0,
    burst_type=1,
    bodyshot_damage=50,
    headshot_damage=91,
    rpm=120,
)

drang = Weapon(
    name="drang",
    mid_burst_time_between_shots=0,
    burst_type=1,
    headshot_damage=50.5,
    bodyshot_damage=36.0,
    rpm=300,
)

piece_of_mind = Weapon(
    name="piece_of_mind",
    mid_burst_time_between_shots=60.0 / 900.0,
    burst_type=3,
    headshot_damage=23.8,
    bodyshot_damage=14,
    rpm=540,
)

dmt = Weapon(
    name="dmt",
    mid_burst_time_between_shots=60.0 / 900.0,
    burst_type=1,
    headshot_damage=45.5,
    bodyshot_damage=80.5,
    rpm=120,
)

crimson = Weapon(
    name="crimson",
    mid_burst_time_between_shots=60.0 / 600.0,
    burst_type=3,
    headshot_damage=30.5,
    bodyshot_damage=19,
    rpm=415.385,
)
