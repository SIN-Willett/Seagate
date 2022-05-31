!gvar edit 09c5a87d-d24b-40eb-8390-71dfef256398
from avrae import *
from files import *
from rewards import *
from checks import *

<drac2>

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
    my_reward, log_entry = my_reward['acquire'](log_message)
    print(dt_reward(my_reward))
    if checks:
      print(format_rolls(checks, results), '\n\n')
    print(f"XP Log updated:\n{code_line(dump_yaml(log_entry))}")
    print(f'signature:\n{code_line(signature())}')
  else:
    print(dt_reward(my_reward))
    if checks:
      print(format_rolls(checks, results), '\n\n')

  return results, my_reward

</drac2>