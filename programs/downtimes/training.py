# !gvar edit 5e2b4ebe-2ed1-4c4a-8aff-8a833d2f4266
import files
import yaml
import time
import xplog
import checks
import stats
import downtimes

<drac2>
def training_reward(chosen_training, training_cc, completed, actions, cc_delta, xp, cost, tier):
  return reward(
    f'your current progress on "{chosen_training}" is {completed + cc_delta}/{actions}\nyou earn:\n{xp * level} XP ({xp}XP * {level}Lv)\n',
    xp, -cost, None,
    reward_cc(training_cc, cc_delta, actions, reward(f'\nyou now have {tier} in "{chosen_training}"', 0, None, True))
  )

def find_trainings(search):
  search = search.lower()
  return [name for name in TOOLS | LANGS | ARMS if search in name.lower()]

def append_profs(tier, prof):
  paths = {
    'expertise': 'eTools',
    'proficiency': 'pTools',
    'fluency': 'languages'
  }

  path = paths[tier]
  data = get(path)
  if not data:
    character().set_cvar(path, prof)
  else:
    character().set_cvar(path, f'{data}, {prof}')

def main(args):
  if not args:
    err(f'usage: {ctx.prefix}dt train [list] topic [options]')
  search = args.pop(0)
  do_list = search.lower() == 'list'
  if do_list:
    search = args.pop(0)

  test_mode = 'test' in [arg.lower() for arg in args]

  possibilities = find_trainings(search)

  if not possibilities:
    err(f"{search} isn't a valid thing to train in")

  if do_list:
    err(", ".join(possibilities))

  chosen_training = possibilities[0]

  if chosen_training in ETOOLS:
    err(f"You already have expertise in {chosen_training}")
  if chosen_training in PLANGS:
    err(f"You are already fluent in {chosen_training}")
  if chosen_training in PTOOLS:
    actions = 28 - max(intelligenceMod * 2, 0)
    cost = 10
    tier = 'expertise'
  else:
    actions = 14 - max(intelligenceMod, 0)
    cost = 5
    tier = 'fluency' if chosen_training in LANGS else 'proficiency'

  if character()
  training_cc = f"Training: {chosen_training}"
  prev_training = get("DTtraining")
  prev_cc = f"Training: {prev_training}"
  if prev_training != chosen_training or not character().cc_exists(training_cc):
    completed = 0
    if not test_mode:
      if character().cc_exists(prev_cc):
        character().delete_cc(prev_cc)
      character().set_cvar("DTtraining", chosen_training)
  else:
    completed = character().get_cc(training_cc)

  checks = load_checks([(chosen_training, [16, 21])], args)

  max_reward = training_reward(chosen_training, training_cc, completed, actions, 3, 30, cost, tier)
  rewards = {
    0: training_reward(chosen_training, training_cc, completed, actions, 1, 10, cost, tier),
    1: training_reward(chosen_training, training_cc, completed, actions, 2, 15, cost, tier),
    2: max_reward,
    'nat20': max_reward,
  }

  res, rew = do_downtime('training', checks, rewards,
    f'training in {chosen_training}',
    test_mode, 'guid' in args)

  if rew.get('special') and not test_mode:
    append_profs(tier, chosen_training)
    character().delete_cvar("DTtraining")

main(&&&)
</drac2>
&STDEMBED&
-thumb <image>