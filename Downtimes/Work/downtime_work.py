# Gvar  1231c3de-651d-4d19-abfe-185c09b785c7
<drac2>
args = &&&

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
total_gp = (gp * int(work.income))
response = f"You recieve {xp} * {level} = {xp * level} XP and {work.income} * {gp} = {total_gp} GP"
</drac2>

-title "{{name}} is doing the Working Downtime!"
-desc "{{name}} {{message}} at {{work.location}} as {{work.role}}!

**{{work.check}}:** {{myroll}}"
-footer "{{response}}
Made by Omie <3"
-color <color>
-thumb <image>