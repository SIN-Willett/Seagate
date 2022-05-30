!gvar edit 236697b1-d74a-4602-94a0-dbc37d29e4a8
import files
import yaml
import time
import xplog
import checks
import stats
import downtimes

<drac2>

def main(args):
  if not args or len(args) < 2:
    err(f'usage: {ctx.prefix}dt study [list] topic hours [options]')
  chosen_topic = args.pop(0)
  do_list = chosen_topic.lower() == 'list'
  if do_list:
    chosen_topic = args.pop()
    hours = 0
  else:
    hours = int(args.pop(0))
    if hours < 0 or hours > 8:
      err(f"hold on lemme ask Artumir for a time machine we're doing {int(hours * 7.5)}min/hr")

  test_mode = 'test' in [arg.lower() for arg in args]

  topics = get_yaml("g/dd5d5f96-c57f-4294-bd4a-2312c0db2d2e")
  possibilities = [(topic, hours) for (topic, hours) in topics.items() if chosen_topic.lower() in topic.lower()]
  if not possibilities:
    err(f"{chosen_topic} isn't a valid thing to study")
  if do_list:
    topics = [topic for topic, _ in possibilities]
    err(", ".join(topics))
  chosen_topic = possibilities[0][0]
  max_hours = possibilities[0][1]

  topic_cc = f"Study: {chosen_topic}"

  completed_hours = 0 if not character().cc_exists(topic_cc) else character().get_cc(topic_cc)
  total_hours = min(completed_hours + hours, max_hours)

  rewards = {
    0: reward(
      f"""after studying for {hours} hours your current progress on studying "{chosen_topic}" is now {total_hours}/{max_hours} hours!\n""",
      0, None, None,
      reward_cc(
        topic_cc,
        hours,
        max_hours,
        reward(f'''\nyou now know "{chosen_topic}"''')
      )
    )
  }

  do_downtime(
    'studying',
    [],
    rewards,
    f'Studying {chosen_topic} for {hours} hours',
    test_mode,
    'guid' in args
  )
  stdtitle.clear()
  print(f'{character().name} studied {chosen_topic} for {hours}hr!', '', stdtitle)


main(&&&)
</drac2>
&STDEMBED&
-thumb <image>