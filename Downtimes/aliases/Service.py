embed <drac2>
args = &ARGS&

if not args:
    err("Please clarify who you're giving Service to!")
if (args[0] == "adv") or (args[0] == "guid"):
    err("Please clarify who you're giving Service to before arguements!")

who = args[0]

mydice = ""
if "adv" in args:
    mydice += f"2d20kh1+{character().skills.religion.value}"
if "dis" in args:
    mydice += f"2d20kl1+{character().skills.religion.value}"
else:
    mydice += f"1d20+{character().skills.religion.value}"
if "guid" in args:
    mydice += "+1d4[guidance]"

myroll = vroll(mydice)

title = f'does the service downtime to {who}'
output_text = '** Religion: **' + myroll + '\n'

possiblities = load_json(get_gvar("f5554176-d94a-4ba5-a735-425330f8f98c"))
response = ""
if myroll.result.crit == 2:
    response = possiblities[0]
elif myroll.result.total <= 10:
    response = possiblities[1]
elif myroll.result.total <= 15:
    response = possiblities[2]
elif myroll.result.total <= 20:
    response = possiblities[3]
else:
    response = possiblities[4]
    
</drac2>
-title "{{name}} {{title}}"
-desc "{{output_text}}"
-footer "{{response}}
Made by Omie <3"
-color <color>
-thumb <image>