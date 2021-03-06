# Assumes the first shot is always a headshot.
# Assumes accuracy is consistent thereafter (ignores things like accuracy bloom).
# Assumes unlimited mag size.
# Assumes probabilities in Odds class.


# TODO: make a separate function to calculate damage bonuses

from dataclasses import dataclass
import random

import weapons

number_of_gunfights = 10000  # decrease this for faster simulation times; increase for more precise results


@dataclass
class Odds:
    overshield = 0.08  # from barricade OR rift overshield
    restoration = 0.1  # chance restoration is already active on an enemy
    rift = 0.16
    already_damaged = 0.35  # chance the enemy is already weak
    healing_nade_during_fight = 0.03
    wormhusk_during_fight = 0.0251
    classy_restoration_during_fight = 0.05
    loreley_during_fight = 0.04

    bodyshot = 0
    headshot = 0


restoration_x1_hp_per_s = 25
restoration_x2_hp_per_s = 42.5
rift_hp_per_s = 40
healing_nade_heal = 30



class RangeDict(dict):
    def __getitem__(self, item):
        if not isinstance(item, range):
            for key in self:
                if item in key:
                    return self[key]
            raise KeyError(item)
        else:
            return super().__getitem__(item)


def make_weapon():
    burst_type_prompt = "If your gun is semi-auto or automatic, type 1. If your gun is a burst-fire weapon, type the number of bullets per burst. When ready, hit Enter.\n"
    burst_type = input(burst_type_prompt)
    weapon = weapons.Weapon()

    if burst_type == "2":
        weapon.burst_type = 2
        weapon.mid_burst_time_between_shots = 60.0 / 600.0
        # aggressive burst sidearms have a different time between shots, mid-burst than pulse rifles
    elif burst_type == "crimson":
        weapon = weapons.crimson
        # crimson has a different time between shots, mid-burst than pulse rifles
    elif burst_type == "dmt":
        weapon = weapons.dmt
    else:
        weapon.burst_type = int(burst_type)
        weapon.mid_burst_time_between_shots = 60.0 / 900.0

    if weapon.name not in ("crimson", "dmt"):
        if (weapon.burst_type < 1) or (weapon.burst_type > 5):
            raise Exception("Error: invalid number of bullets per burst entered.\n")

    if weapon.name not in ("crimson", "dmt"):
        weapon.bodyshot_damage = float(input("Bodyshot damage?\n"))
        weapon.headshot_damage = float(input("Headshot damage?\n"))
        weapon.rpm = float(input("RPM?\n"))

    return weapon


def getRandomHP():
    hp_per_resil = {
        1: 186,
        2: 187,
        3: 188,
        4: 189,
        5: 190,
        6: 192,
        7: 194,
        8: 196,
        9: 198,
        10: 200,
    }
    resilience = random.randint(1, 10)
    return hp_per_resil[resilience]


def getOvershield():
    overshield = 0.0
    if random.random() < Odds.overshield:
        num = random.random()
        if num < 0.375:  # 3 in 8 chance the overshield is a full barricade overshield
            overshield = 45.0
        elif num < 0.875:  # 4 in 8 chance it's a warlock rift overshield
            overshield = random.triangular(0.0, 17.0, 0.0)
        else:  # 1 in 8 chance it's a partial barricade overshield
            overshield = random.triangular(0.0, 45.0, 0.0)
        return overshield
    else:
        return overshield


def getInitialDamage():
    initial_dmg = 0
    if random.random() < Odds.already_damaged:
        weapon_type_chance = random.random()
        if weapon_type_chance < 0.074:
            # damaged by a 140 hc, the most common damage source
            bodyshot_dmg = 46.33
            headshot_dmg = 69.4
            hc_damage_odds = RangeDict(
                {
                    range(0, 22): headshot_dmg,
                    range(22, 36): bodyshot_dmg,
                    range(36, 61): headshot_dmg + bodyshot_dmg,
                    range(61, 82): headshot_dmg * 2,
                    range(82, 100): bodyshot_dmg * 2,
                }
            )
            adaptive_hc_damage_chance = random.randint(0, 99)
            initial_dmg = hc_damage_odds[adaptive_hc_damage_chance]
        elif weapon_type_chance < 0.109:
            # bodied by an adaptive sniper, the second most common damage source
            initial_dmg = 130.5
        else:  # random source of damage from 10 to 184
            initial_dmg = random.randint(10, 184)
    return initial_dmg


# TODO: make a generic healing effect with an intensity and duration
def getInitialHealing():
    restoration_x1_duration = 0.0
    restoration_x2_duration = 0.0
    if random.random() < Odds.restoration:  # restoration active
        if random.random() < 0.67:  # 2/3 chance it's restoration x1, 1/3 it's x2
            restoration_x1_duration = random.random() * 6.0
        else:
            restoration_x2_duration = random.random() * 6.0
    if random.random() < Odds.rift:
        rift_active = True
    else:
        rift_active = False
    return restoration_x1_duration, restoration_x2_duration, rift_active


def getMidFightHeals():
    healing_nade_proc_hp = None
    wormhusk_proc_hp = None
    classy_proc_hp = None
    loreley_proc_hp = None

    def get_thresh():
        thresh = None
        while not thresh:
            thresh = random.gauss(92.5, 30)
            if thresh >= 185 or thresh <= 0:
                thresh = None
        return thresh

    if random.random() < Odds.healing_nade_during_fight:
        healing_nade_proc_hp = get_thresh()

    if random.random() < Odds.wormhusk_during_fight:
        wormhusk_proc_hp = get_thresh()

    if not wormhusk_proc_hp or wormhusk_proc_hp < 0:
        if random.random() < Odds.classy_restoration_during_fight:
            classy_proc_hp = get_thresh()

    if not (wormhusk_proc_hp or classy_proc_hp):
        if random.random() < Odds.loreley_during_fight:
            loreley_proc_hp = 70.0

    return healing_nade_proc_hp, wormhusk_proc_hp, classy_proc_hp, loreley_proc_hp


def get_avg_ttk(weapon, iterations):
    tot_ttk = 0.0

    for _ in range(iterations):
        ttk = gunfight(weapon)
        tot_ttk += ttk

    avg_ttk = tot_ttk / iterations
    return avg_ttk


def gunfight(weapon):
    def refresh_resto():
        """refresh 2x restoration if it exists, otherwise add 1x restoration"""
        if restoration_x2_duration > 0:
            return 0, 6
        return 6, 0

    enemy_hp = getRandomHP() + getOvershield() - getInitialDamage()
    restoration_x1_duration, restoration_x2_duration, rift_active = getInitialHealing()
    (
        healing_nade_proc_hp,
        wormhusk_proc_hp,
        classy_proc_hp,
        loreley_proc_hp,
    ) = getMidFightHeals()
    total_shots = 0  # total shots this fight
    ttk = 0.0  # total time taken to eliminate opponent this fight

    # how many headshots have been hit this fight (used for dmt)
    headshots = round(random.random())

    # shoot one headshot initially
    if weapon.name == "dmt":
        enemy_hp -= weapon.headshot_damage + headshots * 3.22
    else:
        enemy_hp -= weapon.headshot_damage
    headshots += 1
    total_shots += 1

    while enemy_hp >= 0:
        # if the time between the previous shot and this shot is the mid-burst time
        tick_time = weapon.mid_burst_time_between_shots
        if total_shots % weapon.burst_type == 0:
            # else if the time between the previous shot and this shot is the between-bursts time
            tick_time = weapon.get_time_between_shots()

        ttk += tick_time

        # heal from restoration x1
        enemy_hp += restoration_x1_hp_per_s * min(tick_time, restoration_x1_duration)

        # heal from restoration x2
        enemy_hp += restoration_x2_hp_per_s * min(tick_time, restoration_x2_duration)

        # heal from rift
        if rift_active:
            enemy_hp += rift_hp_per_s * tick_time

        restoration_x1_duration -= min(tick_time, restoration_x1_duration)
        restoration_x2_duration -= min(tick_time, restoration_x2_duration)

        # check for mid fight heals
        # healing nade
        if healing_nade_proc_hp and enemy_hp < healing_nade_proc_hp:
            enemy_hp += healing_nade_heal
            if random.random() < 0.67:  # restoration x1
                restoration_x1_duration, restoration_x2_duration = refresh_resto()
            else:  # restoration x2
                restoration_x1_duration = 0.0
                restoration_x2_duration = 6.0
            healing_nade_proc_hp = None
        # wormhusk, assumes classy
        if wormhusk_proc_hp and enemy_hp < wormhusk_proc_hp:
            enemy_hp += 67
            restoration_x1_duration, restoration_x2_duration = refresh_resto()
            wormhusk_proc_hp = None
        # classy
        if classy_proc_hp and enemy_hp < classy_proc_hp:
            restoration_x1_duration, restoration_x2_duration = refresh_resto()
            classy_proc_hp = None
        # loreley
        if loreley_proc_hp and enemy_hp < loreley_proc_hp:
            restoration_x1_duration = 0.0
            restoration_x2_duration = 6.0
            loreley_proc_hp = None

        # hit head, hit body, or miss
        shot_location = random.randint(0, 100)
        if shot_location < Odds.bodyshot:
            if weapon.name == "dmt":
                enemy_hp -= weapon.bodyshot_damage + (headshots) * 1.82
            else:
                enemy_hp -= weapon.bodyshot_damage

        elif shot_location < (Odds.bodyshot + Odds.headshot):
            if weapon.name == "dmt":
                enemy_hp -= weapon.headshot_damage + (headshots) * 3.22
            else:
                enemy_hp -= weapon.headshot_damage
            headshots += 1

        total_shots += 1
    return ttk


if __name__ == "__main__":
    Odds.headshot = float(input("Percent chance to headshot?\n"))
    Odds.bodyshot = float(input("Percent chance to bodyshot?\n"))
    weapon = make_weapon()
    avg_ttk = get_avg_ttk(weapon, number_of_gunfights)
    avg_ttk = format(avg_ttk, ".3f")
    print(f"Avg TTK of your gun under these circumstances is: {avg_ttk}s")
