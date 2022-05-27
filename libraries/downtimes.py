!gvar edit 09c5a87d-d24b-40eb-8390-71dfef256398
<drac2>

def reward_cc(cc_name, cc_delta, cc_max, cc_reward):
  return {
    'name': cc_name,
    'delta': cc_delta,
    'max': cc_max,
    'reward': cc_reward
  }

def reward(message=None, xp=0, gp=None, items=None, r_cc=None):
  return {
    'msg': message,
    'xp': xp,
    'gp': gp,
    'items': items,
    'r_cc': r_cc
    }

def reward_add(r1, r2):
  if not r1:
    return r2
  if not r2:
    return r1
  return r1 + r2

def sum_rewards(this, other):
  if not this:
    return other
  if not other:
    return this

  return reward(
    reward_add(this.msg, other.msg),
    reward_add(this.xp, other.xp),
    reward_add(this.gp, other.gp),
    reward_add(this['items'], other['items']),
    this.r_cc)

def split_coin(gold):
  if not gold:
    return 0,0,0

  gp = int(gold)
  gold -= gp
  sp = int(gold * 10)
  gold -= sp / 10
  cp = int(gold * 100)
  gold -= cp / 100
  cp += (gold > 0)

  return gp, sp, cp

def acquire_cc(my_cc):
  if not character().cc_exists(my_cc.name):
    character().create_cc_nx(my_cc.name, maxVal=my_cc.max, initial_value=0)

  character().mod_cc(my_cc.name, my_cc.delta)
  curr = character().get_cc(my_cc.name)
  max_val = character().get_cc_max(my_cc.name)

  if curr >= max_val:
    character().delete_cc(my_cc.name)
    return my_cc.reward
  return None

def acquire_reward(my_reward, msg):
  if my_reward.r_cc:
    cc_reward = acquire_cc(my_reward.r_cc)
    my_reward = sum_rewards(my_reward, cc_reward)

  log_entry = log_xp(my_reward.xp, msg)
  gp, sp, cp = split_coin(my_reward.gp)
  character().coinpurse.modify_coins(0, gp, 0, sp, cp)

  return my_reward, log_entry

def get_reward(results, rewards):
  if 'nat20' in rewards:
    my_reward = rewards.pop('nat20')
    if results.nat20:
      return my_reward

  if 'fail' in rewards:
    my_reward = rewards.pop('fail')
    if results.fail:
      return my_reward

  return rewards[results.vp]

def dt_title(dt_name, is_testing):
  return f'''{character().name} {'tested' if is_testing else 'did'} the {dt_name} downtime'''

def dt_reward(my_reward):
  return code_block(f'{my_reward.msg}', 'prolog')

def do_downtime(dt_name, checks, rewards, log_message, test_mode, guid):
  guid = guid or "Guidance" in character().spellbook
  results = roll_checks(checks, guid)
  my_reward = get_reward(results, rewards)

  print(dt_title(dt_name, test_mode), '', stdtitle)

  if not test_mode:
    my_reward, log_entry = acquire_reward(my_reward, log_message)
    print(dt_reward(my_reward))
    if checks:
      print(format_rolls(checks, results), '\n\n')
    print(f"XP Log updated:\n{code_line(dump_yaml(log_entry))}")
    print(f'signature:\n{code_line(signature())}')
  else:
    print(dt_reward(my_reward))
    if checks:
      print(format_rolls(checks, results), '\n\n')

</drac2>