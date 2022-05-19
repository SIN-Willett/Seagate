# Gvar  1231c3de-651d-4d19-abfe-185c09b785c7
<drac2>
args = &&&
pars = argparse(args).last

registered = get("Work")
if not registered:
    err("You need to set what you do for work using !work")

work = load_json(get("Work"))
if not work:
    err("You need to set what you do for work using !work")

using = work.check

tool = 0
if ("exp" in args) or (using.lower() in get('eTools','').lower()):
    tool += ((proficiencyBonus) * 2)
elif ("prof" in args) or (using.lower() in get('pTools','').lower()):
    tool += (proficiencyBonus)

checks = load_json(get("stats"))
modifier = checks[using].mod
message = checks[using].message
is_tool = checks[using].is_tool

mymodifier = modifier + tool

mydice = ""
if "adv" in args:
    mydice += f"2d20kh1+{mymodifier}"
elif "dis" in args:
    mydice += f"2d20kl1+{mymodifier}"
else:
    mydice += f"1d20+{mymodifier}"
if "guid" in args:
    mydice += "+1d4[guidance]"
if "ls" in args and is_tool:
    mydice += "+1[luckstone]"
if "-b" in args or "-bonus" in args:
    bonus = pars("b", pars("bonus",""))
    mydice += ("+" + bonus + "[bonus]")
    
myroll = vroll(mydice)

xp = []
gp = []
if (myroll.result.crit == 1):
    xp = 45
    gp = 1.5
elif myroll.result.total < 10:
    xp = 15
    gp = 0.5
else:
    xp = 30
    gp = 1
total_earned = (gp * int(work.income))

gp_gained = floor(total_earned)
sp_gained = int((total_earned - gp_gained) * 10)

character().coinpurse.modify_coins(0, gp_gained, 0, sp_gained)

total_gp = character().coinpurse.get_coins()["gp"]
total_sp = character().coinpurse.get_coins()["sp"]


xp_table = load_json(get_gvar("1735dc7f-fedd-4d83-8a37-584ca6c55d02"))

exp_cc = "Experience"
level = level
next_level = level + 1
message = ""

if character().get_cc(exp_cc) >= xp_table[str(next_level)]:
    message = f"\nYou have leveled up to {next_level}!"
    level = next_level

total_xp = (xp * level)
xp_args = str(total_xp + " | Work downtime at " + work.location)

xplog = load_json(get('xplog','{}'))
timestamp = get("Timestamp")
xplog.update({timestamp:xp_args})
character().set_cvar('xplog',dump_json(xplog))
character().mod_cc(exp_cc,total_xp)

char_xp = character().get_cc(exp_cc)

response = f"You recieve {xp} * {level} = {total_xp} XP and {work.income} * {gp} = "
coin_response = f"You now have {char_xp} XP and "
xplog_response = f"Your most recent xplog entry will be:"

if sp_gained != 0:
    response += f"{gp_gained} GP + {sp_gained} SP!"
    coin_response += f"{total_gp} GP + {total_sp} SP!"
else:
    response += f"{gp_gained} GP!"
    coin_response += f"{total_gp} GP!"

</drac2>

-title "{{name}} is doing the Working Downtime!"
-desc "{{name}} {{message}} at {{work.location}} as {{work.role}}!

**{{work.check}}:** {{myroll}}"
-footer "{{response}}

{{coin_response}}

{{xplog_response}}{{message}}
{{timestamp}}: {{xp_args}}

Made by Omie <3"
-color <color>
-thumb <image>
