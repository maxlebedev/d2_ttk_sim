#Assumes the first shot is always a headshot. 
#Assumes accuracy is consistent thereafter (ignores things like accuracy bloom).
#Assumes unlimited mag size.
#Assumes probabilities in lines 11-18.


# TODO: make a separate function to calculate damage bonuses

from dataclasses import dataclass
import random

number_of_gunfights = 10000 #decrease this for faster simulation times; increase for more precise results

overshield_chance = 0.08 #from barricade OR rift overshield
restoration_chance = 0.1 #chance restoration is already active on an enemy
rift_chance = 0.16 
already_damaged_chance = 0.35 #chance the enemy is already weak
healing_nade_during_fight_chance = 0.03
wormhusk_during_fight_chance = 0.0251
classy_restoration_during_fight_chance = 0.05
loreley_during_fight_chance = 0.04

restoration_x1_hp_per_s = 25
restoration_x2_hp_per_s = 42.5
rift_hp_per_s = 40
healing_nade_heal = 30

bodyshot_chance = 0
headshot_chance = 0

@dataclass
class Weapon:
  name: str = ""
  mid_burst_time_between_shots: int = 0
  burst_type: int = 0
  rpm: int = 0
  headshot_damage: int = 0
  bodyshot_damage: int = 0

  @property
  def get_time_between_shots(self):
    ret = 60.0*self.burst_type/self.rpm - (self.burst_type - 1)*self.mid_burst_time_between_shots #time between shots, between bursts
    return ret


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
  burst_type = int(input("If your gun is semi-auto or automatic, type 1. If your gun is a burst-fire weapon, type the number of bullets per burst. When ready, hit Enter.\n"))
  weapon = Weapon()

  if burst_type == "2": 
    weapon.burst_type = 2
    weapon.mid_burst_time_between_shots = 60.0/600.0 #time between shots, mid-burst; aggressive burst sidearms have a different time between shots, mid-burst than pulse rifles
  elif burst_type == "crimson":
    weapon.name = "crimson"
    weapon.burst_type = 3
    weapon.bodyshot_damage = 19.0
    weapon.headshot_damage = 30.5
    weapon.rpm = 415.385
    weapon.mid_burst_time_between_shots = 60.0/600.0 #time between shots, mid-burst; crimson has a different time between shots, mid-burst than pulse rifles
  elif burst_type == 'dmt':
    weapon.name = "dmt"
    weapon.burst_type = 1
    weapon.bodyshot_damage = 45.5
    weapon.headshot_damage = 80.5
    weapon.rpm = 120
  else:
    weapon.burst_type = int(burst_type)
    weapon.mid_burst_time_between_shots = 60.0/900.0 #time between shots, mid-burst
  if weapon.name not in ("crimson", "dmt"):
    if (weapon.burst_type < 1) or (weapon.burst_type > 5):
      raise Exception('Error: invalid number of bullets per burst entered.\n')

  if weapon.name not in ("crimson", "dmt"):
    weapon.bodyshot_damage = float(input('Bodyshot damage?\n'))
    weapon.headshot_damage = float(input('Headshot damage?\n'))
    weapon.rpm = float(input('RPM?\n'))
  
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
    10: 200
  }
  resilience = random.randint(1, 10)
  return hp_per_resil[resilience]


def getOvershield():
  overshield = 0.0
  if random.random() < overshield_chance: 
    num = random.random()
    if num < 0.375: #3 in 8 chance the overshield is a full barricade overshield
      overshield = 45.0
    elif 0.375 <= num < 0.875: #4 in 8 chance it's a warlock rift overshield
      overshield = random.triangular(0.0,17.0,0.0)
    else: #1 in 8 chance it's a partial barricade overshield
      overshield = random.triangular(0.0,45.0,0.0)
    return overshield
  else:
    return overshield

def getInitialDamage():
  initial_dmg = 0
  if random.random() < already_damaged_chance:
    weapon_type_chance = random.random()
    if weapon_type_chance < 0.074: #damaged by a 140 hc, the most common damage source
      bodyshot_dmg = 46.33
      headshot_dmg = 69.4
      hc_damage_odds = RangeDict({
        range(0,22): headshot_dmg,
        range(22,36): bodyshot_dmg,
        range(36,61): headshot_dmg + bodyshot_dmg,
        range(61,82): headshot_dmg * 2,
        range(82,100): bodyshot_dmg * 2
      })
      adaptive_hc_damage_chance = random.randint(0,99)
      initial_dmg = hc_damage_odds[adaptive_hc_damage_chance]
    elif weapon_type_chance < 0.109: #bodied by an adaptive sniper, the second most common damage source
      initial_dmg = 130.5
    else: #random source of damage from 10 to 184
      initial_dmg = random.randint(10, 184)
  return initial_dmg

# TODO: replace with like a 'heal' intensite value or something
def getInitialHealing():
  restoration_x1_duration = 0.0
  restoration_x2_duration = 0.0
  if random.random() < restoration_chance: #restoration active
    if random.random() < 0.67: #2/3 chance it's restoration x1, 1/3 it's x2
      restoration_x1_duration = random.random()*6.0
    else:
      restoration_x2_duration = random.random()*6.0
  if random.random() < rift_chance:
    rift_active = True
  else:
    rift_active = False
  return restoration_x1_duration, restoration_x2_duration, rift_active

def getMidFightHeals():
  healing_nade_proc_hp = -1000.0 #-1000 chosen arbitrarily as some hp value that will never be reached
  wormhusk_proc_hp = -1000.0
  classy_proc_hp = -1000.0
  loreley_proc_hp = -1000.0

  if random.random() < healing_nade_during_fight_chance:
    while (healing_nade_proc_hp <= 0):
      healing_nade_proc_hp = random.gauss(92.5,30) #assume people heal around mid hp
      if healing_nade_proc_hp >= 185.0:
        healing_nade_proc_hp = -1000.0
        
  if random.random() < wormhusk_during_fight_chance:
    while (wormhusk_proc_hp <= 0):
      wormhusk_proc_hp = random.gauss(92.5,30)
      if wormhusk_proc_hp >= 185.0:
        wormhusk_proc_hp = -1000.0
        
  if wormhusk_proc_hp < 0:
    if random.random() < classy_restoration_during_fight_chance:
      while (classy_proc_hp <= 0):
        classy_proc_hp = random.gauss(92.5,30)
        if classy_proc_hp >= 185.0:
          classy_proc_hp = -1000.0
        
  if (wormhusk_proc_hp < 0) and (classy_proc_hp < 0):
    if random.random() < loreley_during_fight_chance:
      loreley_proc_hp = 70.0

  return healing_nade_proc_hp, wormhusk_proc_hp, classy_proc_hp, loreley_proc_hp


def get_ttk(weapon):
  tot_ttk = 0.0 #sum of all TTKs thus far

  for _ in range(number_of_gunfights):
    ttk = gunfight(weapon)
    tot_ttk += ttk #add this gunfight's ttk to the totalTTK

  avg_ttk = tot_ttk/number_of_gunfights
  return avg_ttk

def gunfight(weapon):
  enemy_hp = getRandomHP() + getOvershield() - getInitialDamage()
  original_hp = enemy_hp
  restoration_x1_duration, restoration_x2_duration, rift_active = getInitialHealing()
  healing_nade_proc_hp, wormhusk_proc_hp, classy_proc_hp, loreley_proc_hp = getMidFightHeals()
  totShots = 0 #total shots this fight
  ttk = 0.0 #total time taken to eliminate opponent this fight
  headshots = round(random.random()) #how many headshots have been hit this fight (used for dmt)

  #shoot one headshot initially
  if weapon.name == "dmt":
    enemy_hp -= weapon.headshot_damage + headshots*3.22
  else:
    enemy_hp -= weapon.headshot_damage
  headshots += 1
  totShots += 1  

  #now start counting ttk for this gunfight
  while enemy_hp >= 0: #shoot one shot at a time
    #consider time since last shot

    #if the time between the previous shot and this shot is the mid-burst time
    tick_time = weapon.mid_burst_time_between_shots
    if totShots%weapon.burst_type == 0: #else if the time between the previous shot and this shot is the between-bursts time
      tick_time = weapon.get_time_between_shot

    ttk += tick_time
    #heal from restoration x1
    if tick_time < restoration_x1_duration:
      enemy_hp += restoration_x1_hp_per_s*tick_time
    else:
      enemy_hp += restoration_x1_hp_per_s*restoration_x1_duration
    #heal from restoration x2
    if tick_time < restoration_x2_duration:
      enemy_hp += restoration_x2_hp_per_s*tick_time
    else:
      enemy_hp += restoration_x2_hp_per_s*restoration_x2_duration
    #heal from rift
    if rift_active:
      enemy_hp += rift_hp_per_s*tick_time

    restoration_x1_duration -= min(tick_time, restoration_x2_duration)
    restoration_x2_duration -= min(tick_time, restoration_x2_duration)


    
    #check for mid fight heals
    #healing nade
    if enemy_hp < healing_nade_proc_hp: 
      enemy_hp += 30
      if random.random() < 0.67: #restoration x1
        if restoration_x2_duration > 0:
          restoration_x1_duration = 0.0 
          restoration_x2_duration = 6.0 #refresh
        else:
          restoration_x1_duration = 6.0
          restoration_x2_duration = 0.0
      else: #restoration x2
        restoration_x1_duration = 0.0
        restoration_x2_duration = 6.0
      healing_nade_proc_hp = -1000.0
    #wormhusk, assumes classy
    if enemy_hp < wormhusk_proc_hp: 
      enemy_hp += 67
      if restoration_x2_duration > 0:
        restoration_x1_duration = 0.0 
        restoration_x2_duration = 6.0 #refresh
      else:
        restoration_x1_duration = 6.0
        restoration_x2_duration = 0.0
      wormhusk_proc_hp = -1000.0
    #classy
    if enemy_hp < classy_proc_hp: 
      if restoration_x2_duration > 0:
        restoration_x1_duration = 0.0 
        restoration_x2_duration = 6.0 #refresh
      else:
        restoration_x1_duration = 6.0
        restoration_x2_duration = 0.0
      classy_proc_hp = -1000.0
    #loreley
    if enemy_hp < loreley_proc_hp: 
      restoration_x1_duration = 0.0 
      restoration_x2_duration = 6.0
      loreley_proc_hp = -1000.0

    #hit head, hit body, or miss
    num = random.random()
    if num < bodyshot_chance: #if this shot is a bodyshot
      if weapon.name == "dmt":
        enemy_hp -= weapon.bodyshot_damage + (headshots)*1.82
      else:
        enemy_hp -= weapon.bodyshot_damage

    elif bodyshot_chance <= num < (bodyshot_chance + headshot_chance): #if this shot is a headshot
      if weapon.name == "dmt":
        enemy_hp -= weapon.headshot_damage + (headshots)*3.22
      else:
        enemy_hp -= weapon.headshot_damage
      headshots += 1
    
    #else: do nothing; it's a miss
    
    totShots += 1
  print(f"enemy hp: {original_hp} ttk: {ttk}")
  return ttk

if __name__ == "__main__":
  headshot_chance = float(input('Chance to headshot?\n'))/100.0
  bodyshot_chance = float(input('Chance to bodyshot?\n'))/100.0
  weapon = make_weapon()
  avg_ttk = get_ttk(weapon)
  print('Avg TTK of your gun under these circumstances is:\n',format(avg_ttk,'.3f'),'s')