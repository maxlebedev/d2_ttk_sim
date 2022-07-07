import ttk_sim

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