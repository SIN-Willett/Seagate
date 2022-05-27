!gvar edit 9a1fb940-23d6-410e-88df-13eda156dd3e
import files
import yaml
import time
import xplog
import checks
import stats
import downtimes
import dtdefault

<drac2>

def main(args):
  if len(args) < 2:
    err(f'usage: {ctx.prefix}dt downtime dc [options]')
  dt_name = args.pop(0)
  dc = int(args.pop(0))

  test_mode = 'test' in [arg.lower() for arg in args]

  checks = load_checks(find_checks(dt_name, dc), args)
  rewards = default_rewards(len(checks) == 3, dc)

  do_downtime(
    dt_name,
    checks,
    rewards,
    f'downtime {dt_name} at DC: {dc}',
    test_mode,
    'guid' in args
  )


main(&&&)
</drac2>
&STDEMBED&
-thumb <image>