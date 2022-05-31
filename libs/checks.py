!gvar edit 11519649-cd49-4e98-baa7-0ae8e3c67a48
from avrae import *
from stats import *

<drac2>
def load_check(stat_name, thresholds, args, check_num):
  parse = argparse(args).last
  bonus = parse('b') or \
    parse('bonus') or \
    parse(f'b{check_num}') or \
    parse(f'bonus{check_num}')
  bonus = int(bonus) if bonus else None

  return {
    'stat': stat_name,
    'dcs': thresholds,
    'mod': STATS[stat_name].mod,
    'adv': 'adv' in args or f'adv{check_num}' in args,
    'dis': 'dis' in args or f'dis{check_num}' in args,
    'ls': 'ls' in args,
    'bonus': bonus
  }

def load_checks(checks, args):
  return [load_check(check[0], check[1], args, i) for i, check in enumerate(checks)]

def roll_check(check):
  this_roll = ''

  if check.adv:
    this_roll += f'2d20kh1+{check.mod}'
  elif check.dis:
    this_roll += f'2d20kl1+{check.mod}'
  else:
    this_roll += f'1d20+{check.mod}'

  if check.ls:
    this_roll += '+1[luckstone]'

  if check.bonus:
    this_roll += f'+{check.bonus}{[check.bonus]}'

  return vroll(this_roll)

def is_success(rolled, dc):
  # if base roll nat 20d
  if rolled[0].result.crit == 1:
    return True

  # Most updated roll beats dc
  return rolled[-1].total >= dc

def count_vp(checks, rolled):
  vp = 0
  for i, check in enumerate(checks):
    result = rolled[i]
    for threshold in check.dcs:
      if is_success(result, threshold):
        vp += 1
  return vp

def get_highest_check(totals):
  best_total, best = totals[0]
  for total, i in totals:
    if total > best_total:
      best = i
      best_total = total
  return best_total, best

def find_best(checks, results):
  losses = [(r[-1].total, i) for i, r in enumerate(results) if not is_success(r, checks[i].dcs[0])]
  if not losses:
    wins = [(r[-1].total, i) for i, r in enumerate(results) if is_success(r, checks[i].dcs[0])]
    return get_highest_check(wins)
  return get_highest_check(losses)

def get_boosts(checks, rolled, guid):
  if not guid or not rolled:
    return rolled

  total, best = find_best(checks, rolled)
  rolled[best].append(vroll(f"{total}+1d4[guidance]"))
  return rolled

def roll_checks(checks, guid):
  rolled = [[roll_check(check)] for check in checks]
  rolled = get_boosts(checks, rolled, guid)
  vp = count_vp(checks, rolled)
  nat20 = any([result[0].result.crit == 1 for result in rolled])
  fail = not nat20 and any([result[0].result.crit == 2 for result in rolled])
  return {
    'rolls': rolled,
    'vp': vp,
    'nat20': nat20,
    'fail': fail
  }

def format_subroll(check, rollset, part):
  msg = 'Success' if is_success(rollset[:part + 1], check.dcs[0]) else 'Failure'
  left = f"**{check.stat}:** " if part == 0 else '‎ ' * ((len(check.stat) * 2) + 2)
  return f"{left}{rollset[part]} **{msg}!**"

def format_roll(check, rollset):
  chck_lines = [format_subroll(check, rollset, i) for i, r in enumerate(rollset)]
  return '\n'.join(chck_lines)

def format_rolls(checks, results):
  if not checks or not results:
    return ""
  title = []
  if len(checks[0].dcs) == 1:
    title.append(f"**DC:** {checks[0].dcs[0]}")
  else:
    title.append(f"**DCs:** {', '.join([str(dc) for dc in checks[0].dcs])}")

  lines = [format_roll(check, results.rolls[i]) for i, check in enumerate(checks)]
  return '\n'.join(title + lines)
</drac2>