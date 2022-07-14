embed <drac2>
using(libs="02488881-7259-4a76-9362-828df7c35a07")
using(
  io=libs.find_library("io"),
  yaml=libs.find_library("yaml"),
  stats=libs.find_library("stats"),
  xplog=libs.find_library("xplog")
)

LEVEL_THRESHOLDS = [0,300,900,2700,6500,14000,23000,34000,48000,64000,85000,100000,120000,140000,165000,195000,225000,265000,305000,355000,420000]
level = character().levels.total_level

def xp_gain(args):
  if len(args) < 1:
    err("set to what?")
  xp = int(args[0])
  got = "Gained" if xp >= 0 else "Lost"

  msg = f"{got} {max(xp, -xp)}xp" if len(args) == 1 else args[1]
  xplog.log_xp(xp, msg)

  io.print(f"{character().name} {got.lower()} {xp}xp", '', io.stdtitle)

def xp_set(args):
  if len(args) < 2:
    err("set to what?")
  xp = int(args[1])
  msg = f"Total set to {xp}xp" if len(args) == 2 else args[2]

  curr = character().get_cc('Experience')
  io.log_xp(xp - curr, msg)

  io.print(f"{character().name} set {stats.PRONOUNS[2]} xp to {xp}", '', io.stdtitle)

def xp_chart(args):
  lines = [f'{(i + 1) if i < 20 else " Godwoken":9}: {v:,}' for i, v in enumerate(LEVEL_THRESHOLDS)]
  out = ['    level: XP Required ', ('-' * 9) + '+' + ('-' * 13)] + lines
  io.print(io.code_block('\n'.join(out), 'yaml'))

def xp_log_view(args):
  entries_per_page = 40
  logbook = xplog.load_xplog()
  page_count = ceil(len(logbook) / entries_per_page)

  page_num = page_count if len(args) == 1 else int(args[1])

  page_num = min(page_count, max(1, page_num))

  left = entries_per_page * (page_num - 1)
  right = left + entries_per_page

  entries = {k: v for i, (k, v) in enumerate(logbook.items()) if left <= i < right}

  page = xplog.xp_entries_to_str(entries)
  if not page:
    page = "(no entries found)"
  io.print(f"{character().name} viewed {stats.PRONOUNS[2]} xp log", '', io.stdtitle)
  io.print(io.code_block(page), '')
  io.print(io.code_block(f"page {page_num}/{page_count}", 'prolog'))

def xp_status():
  title = f"{character().name} is currently {level}{'st'*(level==1) or 'nd'*(level==2) or 'rd'*(level==3) or 'th'} level!"
  io.print(title, '', io.stdtitle)
  required = LEVEL_THRESHOLDS[level - 1]
  next_level = LEVEL_THRESHOLDS[min(level, 20)]
  xp = xplog.get_xp()
  if required > xp:
    io.print(f"Your experience total needs to be at least {required:,} to match your current level!")
  elif xp >= next_level:
    io.print(f"You have levelled up, it's time to update your sheet with your proper experience total and level then {io.code_line('!update')}")
  io.add_field("Current Experience", xp)
  if xp < LEVEL_THRESHOLDS[-1]:
    io.add_field(f"Next Level: {level + 1 if level < 20 else 'Godwoken'}", f"{next_level:,} *({next_level - xp:,} remaining)*")
  else:
    io.add_field(f"Next Level: Godwoken", f"You can now become godwoken, check out: <#885316318138597436>")

def xp_help(args):
  io.print(io.read_file('g/f7193eab-5e5c-4456-af5f-883c6d7e6b04'))

def main(args):
  args = [x.lower() for x in args]
  character().create_cc_nx(xplog.XP_CC_NAME)

  io.show_thumb()
  if not args:
    xp_status()
  elif args[0] in "chart":
    xp_chart(args)
  elif args[0] in "log":
    xp_log_view(args)
    io.hide_thumb()
  elif args[0] in "set":
    xp_set(args)
  elif args[0] in "help?":
    xp_help(args)
  else:
    xp_gain(args)
  io.print("!xp | !xp # | !xp -# | !xp set # | !xp chart | !xp log | !xp help", '', io.stdfooter)

  return io.stdembed()

return main(&ARGS&)
</drac2>
