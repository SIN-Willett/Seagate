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
  topic = args.pop(0)
  test_mode = 'test' in [arg.lower() for arg in args]

  checks = []

  msgs = get_yaml('g/cc8b0c29-757c-402e-b5c0-1200e7fbe90c', {})
  rewards = {
    0: reward("", 0, None, reward_cc(f"dtsdy-{topic}", ))
  }

  do_downtime(
    'study',
    checks,
    rewards,
    f'downtime service',
    test_mode,
    'guid' in args
  )
  print(f' {topic} }!', '', stdtitle)


main(&&&)
</drac2>
&STDEMBED&
-thumb <image>