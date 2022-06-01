!gvar edit 973373d5-1bf6-4a7a-9b46-afa802cfd4df
from avrae import *
from stats import *
from xplog import *
from files import *

<drac2>
LEVEL_THRESHOLDS = [0,300,900,2700,6500,14000,23000,34000,48000,64000,85000,100000,120000,140000,165000,195000,225000,265000,305000,355000,420000]

def xp_gain(args):
  if len(args) < 1:
    err("set to what?")
  xp = int(args[0])
  got = "Gained" if xp >= 0 else "Lost"

  msg = f"{got} {max(xp, -xp)}xp" if len(args) == 1 else args[1]
  log_xp(xp, msg)

  print(f"{character().name} {got.lower()} {xp}xp", '', stdtitle)

def xp_set(args):
  if len(args) < 2:
    err("set to what?")
  xp = int(args[1])
  msg = f"Total set to {xp}xp" if len(args) == 2 else args[2]

  curr = character().get_cc('Experience')
  log_xp(xp - curr, msg)

  print(f"{character().name} set {PRONOUNS[2]} xp to {xp}", '', stdtitle)

def xp_chart(args):
  lines = [f'{(i + 1) if i < 20 else " Godwoken":9}: {v}' for i, v in enumerate(LEVEL_THRESHOLDS)]
  out = ['    level: XP Required ', ('-' * 9) + '+' + ('-' * 13)] + lines
  print(code_block('\n'.join(out), 'yaml'))

def xp_log_view(args):
  entries_per_page = 40
  logbook = get_yaml(XPLOG_CVAR_NAME, {})
  page_count = ceil(len(logbook) / entries_per_page)

  page_num = page_count if len(args) == 1 else int(args[1])

  page_num = min(page_count, max(1, page_num))

  left = entries_per_page * (page_num - 1)
  right = min(len(logbook), entries_per_page * page_num)

  entries = {k: v for i, (k, v) in enumerate(logbook.items()) if left <= i < right}
  page = xp_entries_to_str(entries)
  if not page:
    page = "(no entries found)"
  print(f"{character().name} viewed {PRONOUNS[2]} xp log", '', stdtitle)
  print(code_block(page), '')
  print(code_block(f"page {page_num}/{page_count}", 'prolog'))

def xp_status():
  title = f"{character().name} is currently {level}{'st'*(level==1) or 'nd'*(level==2) or 'rd'*(level==3) or 'th'} level!"
  print(title, '', stdtitle)
  required = LEVEL_THRESHOLDS[level - 1]
  next_level = LEVEL_THRESHOLDS[min(level, 20)]
  xp = get_xp()
  if required > xp:
    print(f"Your experience total needs to be at least {required:,} to match your current level!")
  elif xp >= next_level:
    print(f"You have levelled up, it's time to update your sheet with your proper experience total and level then {code_line('!update')}")
  add_field("Current Experience", xp)
  if xp < LEVEL_THRESHOLDS[-1]:
    add_field(f"Next Level: {level + 1 if level < 20 else 'Godwoken'}", f"{next_level:,} *({next_level - xp:,} remaining)*")
  else:
    add_field(f"Next Level: Godwoken", f"You can now become godwoken, check out: <#885316318138597436>")

def xp_help(args):
  print(read_file('g/f7193eab-5e5c-4456-af5f-883c6d7e6b04'))

def main(args):
  args = [x.lower() for x in args]
  character().create_cc_nx(XP_CC_NAME)

  show_thumb()
  if not args:
    xp_status()
  elif args[0] in "chart":
    xp_chart(args)
  elif args[0] in "log":
    xp_log_view(args)
    hide_thumb()
  elif args[0] in "set":
    xp_set(args)
  elif args[0] in "help?":
    xp_help(args)
  else:
    xp_gain(args)
  print("!xp | !xp # | !xp -# | !xp set # | !xp chart | !xp log | !xp help", '', stdfooter)

main(&&&)
</drac2>
&STDEMBED&
