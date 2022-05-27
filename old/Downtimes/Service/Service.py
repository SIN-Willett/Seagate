# Gvar e55f5a53-b70a-484d-a386-6acc350d2c0d
<drac2>
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

title = f'does the service downtime to {who}'
output_text = '** Religion: **' + myroll + '\n'

possiblities = load_json(get_gvar("f5554176-d94a-4ba5-a735-425330f8f98c"))
response = ""
xp = 0
total_xp = 0 
if myroll.result.crit == 2:
    response = "You disrespected the temple and are not allowed back for a week."
elif myroll.result.total <= 10:
    response = "You are thanked for your efforts."
elif myroll.result.total <= 15:
    response = "You can now receive one free Ceremony spell if you meet the requirements for it."
elif myroll.result.total <= 20:
    xp = 15
    total_xp = xp * level
    response = "You are granted the effects of the 'Bless' spell for the rest of the day."
else:
    xp = 30
    total_xp = xp * level
    response = "You receive a Holy Symbol of the organization and will receive backing from the temple when attempting to climb political or social ladders."


xp_args = "" + total_xp + " | Service downtime to " + who + " (Roll: " + myroll.result.total + ")"
exp_cc = "Experience"
xplog = load_json(get('xplog','{}'))
timestamp = get("Timestamp")
xplog.update({timestamp:xp_args})
set_cvar('xplog',dump_json(xplog))
mod_cc(exp_cc,total_xp)

char_xp = get_cc(exp_cc)

xplog_response = f"You gain {total_xp} XP and now have {char_xp} XP"

</drac2>
-title "{{name}} {{title}}"
-desc "{{output_text}}"
-footer "{{response}}

{{xplog_response}}
Your most recent xplog entry will be:
{{timestamp}}: {{xp_args}}

Made by Omie <3"
-color <color>
-thumb <image>