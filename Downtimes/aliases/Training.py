embed <drac2>
args = &ARGS&
data = load_json(get_gvar("100f2682-77af-4982-bd1a-cc155b93f262"))
VIPtrainings = load_json(get_gvar("81eb4ed1-4118-4f00-a6f0-4f7e9a070103"))
cc = "Progress"
par = argparse(args[1:])
arg = args[0] if args else None

chosen = None
chosen_category = None
for category, trainings in data.items():
    for training in trainings:
        if arg.lower() in training.lower():
            chosen = training
            chosen_category = category
            break
    if chosen:
        break

if not chosen:
    err("could not find training modifier")

actions = 0
if "exp" in args and chosen in VIPtrainings:
    actions = 28 - (intelligenceMod * 2) if intelligenceMod > 0 else 28
else:
    actions = 14 - intelligenceMod if intelligenceMod > 0 else 14

stats = {
    "strength":strengthMod,
    "dexterity":dexterityMod,
    "intelligence":intelligenceMod,
    "wisdom":wisdomMod,
    "charisma":charismaMod,
    "athletics":character().skills.athletics.value,
}

mydice = ""

if "adv" in args:
    mydice += f"2d20kh1+{stats[chosen_category]}"
elif "dis" in args:
    mydice += f"2d20kl1+{stats[chosen_category]}"
else:
    mydice += f"1d20+{stats[chosen_category]}"
    
if "exp" in args and chosen in VIPtrainings:
    mydice += "+" + proficiencyBonus
if "guid" in args:
    mydice += "+1d4[guidance]"
if "ls" in args and chosen_category != "athletics":
    mydice += "+1[luckstone]"

create_cc_nx(cc,0,actions)
if get("DTtraining") != chosen:
    set_cc(cc,0)
    set_cvar("DTtraining", chosen)
if get_cc(cc) == actions:
    set_cc(cc,0)

myroll = vroll(mydice)
xp = 0
if myroll.total < 16:
    character().mod_cc(cc, +1)
    xp = 10
elif myroll.total < 21:
    character().mod_cc(cc, +2)
    xp = 15
else:
    character().mod_cc(cc, +3)
    xp = 30

checktitle = f' does the training downtime for {chosen}'
response = f'Your current progress on {chosen} is {get_cc(cc)}/{actions}! | You gain {xp} * {level} = {xp * level} XP!'
</drac2>
-title "{{name}} {{checktitle}}"
-desc "{{myroll}}"
-footer "{{response}}
Made by Omen"
-color <color>
-thumb <image>