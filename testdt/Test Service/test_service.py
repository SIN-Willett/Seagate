<drac2>
# gvar 4720b72e-77c9-4f7c-91df-fcb86efe897c
# THIS IS A TEST
args = &&&
pars = argparse(args).last

if not args:
    err("Please clarify who you're giving Service to!")
if (args[1] == "adv") or (args[1] == "guid"):
    err("Please clarify who you're giving Service to before arguements!")

who = args[1]

mydice = ""
if "adv" in args:
    mydice += f"2d20kh1+{character().skills.religion.value}"
elif "dis" in args:
    mydice += f"2d20kl1+{character().skills.religion.value}"
else:
    mydice += f"1d20+{character().skills.religion.value}"
if "guid" in args:
    mydice += "+1d4[guidance]"
if "-b" in args or "-bonus" in args:
    bonus = pars("b", pars("bonus",""))
    mydice += ("+" + bonus + "[bonus]")

myroll = vroll(mydice)

title = f' tests the service downtime to {who}'
output_text = '** Religion: **' + myroll + '\n'

possiblities = load_json(get_gvar("f5554176-d94a-4ba5-a735-425330f8f98c"))
response = ""
xp = 0
total_xp = 0 
if myroll.result.crit == 2:
    response = "If this wasn't a test you would have disrespected the temple and not be allowed back for a week."
elif myroll.result.total <= 10:
    response = "If this wasn't a test you would be thanked for your efforts."
elif myroll.result.total <= 15:
    response = "If this wasn't a test you could now receive one free Ceremony spell if you meet the requirements for it."
elif myroll.result.total <= 20:
    xp = 15
    total_xp = xp * level
    response = "If this wasn't a test you would be granted the effects of the 'Bless' spell for the rest of the day."
else:
    xp = 30
    total_xp = xp * level
    response = "If this wasn't a test you would receive a Holy Symbol of the organization and would receive backing from the temple when attempting to climb political or social ladders."

char_xp = get_cc("Experience")

xplog_response = f"If this wasn't a test you'd gain {xp} * {level} = {total_xp} XP!"

</drac2>
-title "{{name}}{{title}}"
-desc "{{output_text}}"
-footer "{{response}}

{{xplog_response}}
You now have {{char_xp}} XP

Made by Omie <3"
-color <color>
-thumb <image>