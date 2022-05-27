<drac2>
# gvar b378739b-efff-4e99-ae3f-ea00ff58e1d0
# THIS IS A TEST
args = &&&
arg = args[1] if args else None
pars = argparse(args).last

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
cost = 0
VIPtrainings = load_json(get_gvar("81eb4ed1-4118-4f00-a6f0-4f7e9a070103"))

if ("exp" in args and chosen_training in VIPtrainings) or (chosen_training.lower() in p_tools and chosen_training in VIPtrainings):
    actions = 28 - (intelligenceMod * 2) if intelligenceMod > 0 else 28
    mydice += "+" + proficiencyBonus
    cost = 10
else:
    actions = 14 - intelligenceMod if intelligenceMod > 0 else 14
    cost = 5

if "ls" in args and training_tool == True:
    mydice += "+1[luckstone]"
if "guid" in args:
    mydice += "+1d4[guidance]"
if "-b" in args or "-bonus" in args:
    bonus = pars("b", pars("bonus",""))
    mydice += ("+" + bonus + "[bonus]")

bags = load_json(get("bags"))
i = 0
for bag in bags:
    if bag[0] == "Coin Pouch":
        break
    i = i + 1

if i == len(bags):
    err("you have no coin pouch")

gold = bags[i][1].gp
platinum = bags[i][1].pp

cc = "Progress"
character().create_cc_nx(cc, 0, actions)

myroll = vroll(mydice)
xp = 0
successes = 0
if myroll.total < 16:
    successes = 1
    xp = 10
elif myroll.total < 21:
    successes = 2
    xp = 15
else:
    successes = 3
    xp = 30

total_xp = (xp * level)

exp_cc = "Experience"

char_xp = get_cc(exp_cc)

checktitle = f' tests the training downtime for {chosen_training}'
response = f'If this was not a test your current progress on {chosen_training} would be {successes}/{actions}! | You would gain {xp} * {level} = {total_xp} XP!'
coin_response = f"If this wasn't a test training would have cost {cost} GP, but you do have {gold} GP and {platinum} PP in your Coin Pouch."
xplog_response = f"You now have {char_xp} XP"
</drac2>
-title "{{name}}{{checktitle}}"
-desc "{{myroll}}"
-footer "{{response}}

{{coin_response}}

{{xplog_response}}
THIS IS A TEST

Made by Omie <3"
-color <color>
-thumb <image>