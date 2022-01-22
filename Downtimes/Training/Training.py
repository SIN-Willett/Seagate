# Gvar 585d1453-7303-44a5-b736-f707c2702b5e
<drac2>
args = &&&
arg = args[1] if args else None

stats = load_json(get("stats"))
training_tool = None
chosen_training = None
for trainings, entries in stats.items():
    for training in entries:
        if arg.lower() in trainings.lower():
            chosen_training = trainings
            training_tool = entries.is_tool
            break
    if training_tool:
        break

if not chosen_training:
    err("Could not find training modifier, are you sure you can train in " + arg + "?")
if training_tool == False:
    err("" + chosen_training + " is a skill, you can't train in skills friend.")

mydice = ""
p_tools = get('pTools','').lower()

if "adv" in args:
    mydice += f"2d20kh1+{stats[chosen_training].mod}"
elif "dis" in args:
    mydice += f"2d20kl1+{stats[chosen_training].mod}"
else:
    mydice += f"1d20+{stats[chosen_training].mod}"

actions = 0
VIPtrainings = load_json(get_gvar("81eb4ed1-4118-4f00-a6f0-4f7e9a070103"))

if ("exp" in args and chosen_training in VIPtrainings) or (chosen_training.lower() in p_tools and is_tool in VIPtrainings):
    actions = 28 - (intelligenceMod * 2) if intelligenceMod > 0 else 28
    mydice += "+" + proficiencyBonus
if "ls" in args and training_tool == True:
    mydice += "+1[luckstone]"
else:
    actions = 14 - intelligenceMod if intelligenceMod > 0 else 14

if "guid" in args:
    mydice += "+1d4[guidance]"

cc = "Progress"
character().create_cc_nx(cc, 0, actions)

if get("DTtraining") != chosen_training:
    character().set_cc(cc, 0, actions)
    set_cvar("DTtraining", chosen_training)
if character().get_cc(cc) == actions:
    character().set_cc(cc, 0, actions)

myroll = vroll(mydice)
xp = 0
if myroll.total < 16:
    character().mod_cc(cc, +1, actions)
    xp = 10
elif myroll.total < 21:
    character().mod_cc(cc, +2, actions)
    xp = 15
else:
    character().mod_cc(cc, +3, actions)
    xp = 30

checktitle = f' does the training downtime for {chosen_training}'
response = f'Your current progress on {chosen_training} is {character().get_cc(cc)}/{actions}! | You gain {xp} * {level} = {xp * level} XP!'
</drac2>
-title "{{name}} {{checktitle}}"
-desc "{{myroll}}"
-footer "{{response}}
Made by Omen"
-color <color>
-thumb <image>