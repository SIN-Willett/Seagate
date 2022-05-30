!gvar edit 0a0a403d-758e-4114-b926-cece4907bf35
import files
import yaml
import time
import xplog
import checks
import stats
import downtimes

<drac2>

def main(args):
  if not args:
    err(f'usage: {ctx.prefix}dt service god [options]')
  god = args.pop(0)
  test_mode = 'test' in [arg.lower() for arg in args]

  checks = load_checks([('Religion', [10, 15, 20])], args)

  msgs = get_yaml('g/cc8b0c29-757c-402e-b5c0-1200e7fbe90c', {})
  rewards = {
    'fail': reward(msgs.disrespect),
    0: reward(msgs.thanked),
    1: reward(msgs.ceremony),
    2: reward(msgs.holy_symbol, 15),
    3: reward(msgs.bless, 30),
    'nat20': reward(msgs.bless, 30),
  }

  do_downtime(
    'service',
    checks,
    rewards,
    f'downtime service to {god}',
    test_mode,
    'guid' in args
  )
  print(f' to {god}', '', stdtitle)


main(&&&)
</drac2>
&STDEMBED&
-thumb <image>