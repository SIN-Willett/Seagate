!gvar edit dd1b0175-c600-4ad6-bf4a-0708e3856722
from avrae import *
from stats import *
from rewards import *
from downtimes import *

<drac2>
def find_checks(dt_name, dc):
  all_dts = get_yaml("g/0d55e007-c9c3-43c8-b5b3-051353ed8797")
  if dt_name not in all_dts:
    err(f"No downtime called {dt_name}")
  our_dt = all_dts[dt_name]

  return [(best_stat(choices), [dc]) for choices in our_dt]

def base_reward(xp, gold):
  gp, sp, cp = split_coin(gold)

  coin_msgs = []
  if gp:
    coin_msgs.append(f"{gp} GP")
  if sp:
    coin_msgs.append(f"{sp} SP")
  if cp:
    coin_msgs.append(f"{cp} CP")

  msg = f"you earn:\n{xp * level} XP ({xp}XP * {level}Lv)\n" \
        f"{' and '.join(coin_msgs)}!"
  return reward(msg, xp, gold)

def legal_rewards(dc):
  dt_data = get_yaml("g/cd374b66-bf6e-4ef9-ac64-d9e213a5c0cb")
  data = dt_data["legal"][str(dc)]

  return {
    0: reward(f"you earn no GP and no Experience. :("),
    1: base_reward(data.XP // 2, data.Gold / 2),
    2: base_reward(int(data.XP), data.Gold),
    'nat20': base_reward(int(data.XP), data.Gold)
  }

def illegal_rewards(dc):
  dt_data = get_yaml("g/cd374b66-bf6e-4ef9-ac64-d9e213a5c0cb")
  data = dt_data["illegal"][str(dc)]

  return {
    0: reward(f"you are now wanted for a DC {vroll(f'{dc}+5').total} crime! Ping A Moderator, and let an admin know to add you to the wanted board."),
    1: reward("you are now wanted for your crimes! Ping A Moderator, and let an admin know to add you to the wanted board."),
    2: base_reward(data.XP // 2, data.Gold / 2),
    3: base_reward(int(data.XP), data.Gold),
    'nat20': base_reward(int(data.XP), data.Gold)
  }

def default_rewards(is_crime, dc):
  return illegal_rewards(dc) if is_crime else legal_rewards(dc)
</drac2>