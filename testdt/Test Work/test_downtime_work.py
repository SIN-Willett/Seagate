<drac2>
# gvar a74d17ca-00a8-4e43-9ceb-3eb35c5c0c9b
# THIS IS A TEST
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
total_earned = (gp * int(work.income))

gp_gained = floor(total_earned)
sp_gained = int((total_earned - gp_gained) * 10)

total_xp = (xp * level)

char_xp = get_cc("Experience")

response = f"If this wasn't a test you would recieve {xp} * {level} = {total_xp} XP and {work.income} * {gp} = "
coin_response = f"You now have {char_xp} XP"
xplog_response = f"THIS IS A TEST"

if sp_gained != 0:
    response += f"{gp_gained} GP + {sp_gained} SP!"
else:
    response += f"{gp_gained} GP!"

</drac2>

-title "{{name}} is testing the Working Downtime!"
-desc "{{name}} is testing {{message}} at {{work.location}} as {{work.role}}!

**{{work.check}}:** {{myroll}}"
-footer "{{response}}

{{coin_response}}

{{xplog_response}}

Made by Omie <3"
-color <color>
-thumb <image>