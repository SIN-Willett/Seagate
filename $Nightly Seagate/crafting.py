<drac2>
# gvar 4bd5ceb6-e82f-4196-be25-988c6c4e2a3d
args = &&&
pars = argparse(args).last
##gvar for items 1st dict "Magic", 2nd dict "Mundane"
craftables = load_json(get_gvar("c28ac8be-d70e-4842-8f5c-b9e251ce4eb6"))
inputcraft = args[1]
crafting_details = None
item_name = None
crafting_type = None

for craftableCategory, stuff in craftables.items():
    if crafting_details:
        break
        
    for craftableName, craftableDetails in stuff.items():
        if (inputcraft.lower() == craftableName.lower()):
            item_name = craftableName
            crafting_details = craftableDetails
            crafting_type = craftableCategory
        elif (inputcraft.lower() in craftableName.lower()):
            item_name = craftableName
            crafting_details = craftableDetails
            crafting_type = craftableCategory
            break
    
if not crafting_details:
# name not in list
    err("You have failed to select a craftable, please check the name of the item you want to craft against the crafting spreadsheet <3")

magic_data = {
	"Common"	:	{"actions": 7, "price": 100, "ss": 1, "ss_art": 1},
	"Uncommon"	:	{"actions": 15, "price": 200, "ss": 3, "ss_art": 2},
	"Rare"		:	{"actions": 40, "price": 1000, "ss": 5, "ss_art": 3},
	"Very Rare"	:	{"actions": 120, "price": 2000, "ss": 6, "ss_art": 4},
	"Legendary"	:	{"actions": 300, "price": 20000, "ss": 9, "ss_art": 5}
}

rarity = None
price = None
tool = None
actions = None
ss      = None
ss_art  = None

if crafting_type == "Magic":
    rarity  = crafting_details.rarity
    tool    = crafting_details.tool
    actions = magic_data[rarity].actions
    price    = magic_data[rarity].price
    ss      = magic_data[rarity].ss
    ss_art  = magic_data[rarity].ss_art
else:
    price   = crafting_details.price
    tool    = crafting_details.tool
    actions = ceil(price / 10)

# makes the minimum 1 action
if actions < 1:
    actions = 1
# makes the actions 3 for house related things
if not price:
    actions = 3

cc = "Crafting: " + item_name

##makes counter if it doesn't already exist
character().create_cc_nx(cc, 0, actions, None, None, 0)
if (get_cc(cc) == actions) or (price == 0):
    character().set_cc(cc, 0)
    
##cvar for tool to attribute matching
stats = load_json(get("stats"))
mod = stats[tool].mod
arcana = character().skills.arcana.bonus + (character().skills.arcana.prof * proficiencyBonus)
magic_response = None
        
artificer_level = 0
for (cls, class_level) in character().levels:
    if cls == "Artificer":
        if class_level > 1:
            artificer_level = class_level
            ss = ss_art
    break

if crafting_type == "Magic":
    mod += int(arcana)
    if character().spellbook.get_slots(ss) < 1:
        err("You do not have enough spell slots remaining")
    else:
        character().spellbook.use_slot(ss)
        magic_response = f"You use a spell slot for crafting: {character().spellbook.slots_str(ss)}"
if crafting_type == "Mundane":
    if ("exp" in args) or (tool.lower() in get('eTools','').lower()):
        mod += ((proficiencyBonus) * 2)
    elif ("prof" in args) or (tool.lower() in get('pTools','').lower()):
        mod += (proficiencyBonus)

mydice = ""
if "adv" in args:
    mydice += f"2d20kh1+{mod}"
elif "dis" in args:
    mydice += f"2d20kl1+{mod}"
else:
    mydice += f"1d20+{mod}"
if "guid" in args:
    mydice += "+1d4[guidance]"
if "ls" in args and crafting_type == "Mundane":
    mydice += "+1[luckstone]"
if "-b" in args or "-bonus" in args:
    bonus = pars("b", pars("bonus",""))
    mydice += ("+" + bonus + "[bonus]")

myroll = vroll(mydice)

cost = (price * 0.5)
sell = round((price * 0.75), 2)
magic_item_adept = False
if (rarity == "Common") or (rarity == "Uncommon"):
    magic_item_adept = True
registered = get("Guild")
if "guild" in args or registered:
    cost = (cost * 0.75)

xp = 0

def reward(dice_0, dice_1, dice_2, xp_value, cc_1, cc_2, cc_3, cost_mod):
    if myroll.total < dice_0:
        xp = 0
    elif myroll.total < dice_1:
        character().mod_cc(cc, +cc_1)
        xp = xp_value
        cost = (cost * cost_mod)
    elif myroll.total < dice_2:
        character().mod_cc(cc, +cc_2)
        xp = xp_value
        cost = (cost * cost_mod)
    else:
        character().mod_cc(cc, +cc_3)
        xp = xp_value
        cost = (cost * cost_mod)

if crafting_type is "Mundane":
    reward(10, 16, 21, 15, 1, 2, 3, 1)
elif (artificer_level >= 10) and (magic_item_adept is True):
    reward(15, 21, 26, 30, 4, 8, 12, 0.5) 
else:
    reward(15, 21, 26, 30, 1, 2, 3, 1) 

total_xp = xp * level

current_actions = character().get_cc(cc)
xp_args = f" {total_xp} | {cc} ({current_actions}/{actions})"
exp_cc = "Experience"
xplog = load_json(get('xplog','{}'))
timestamp = get("Timestamp")
xplog.update({timestamp:xp_args})
set_cvar('xplog',dump_json(xplog))
mod_cc(exp_cc,total_xp)

char_xp = get_cc(exp_cc)

xplog_response = f"You now have {char_xp} XP and your most recent xplog entry will be:"

title = f'{name} does the crafting downtime for {item_name}'

response_xp = ()
if xp == 0:
    response_xp = f"You failed crafting and gain no xp"
else:
    response_xp = f"Gain {xp} * {level} = {total_xp} XP!"
</drac2>
-title "{{title}}"
-desc "**{{tool}}:** {{myroll}}

Your progress on crafting this is now __{{current_actions}}/{{actions}}__!
{{magic_response}}"
-footer "{{response_xp}}

This item costs {{round(cost, 2)}} GP to make and sells to players for {{price}} GP and to the void for {{sell}} GP!

{{xplog_response}}
{{timestamp}}: {{xp_args}}

Made by Omie <3"
-color <color>
-thumb <image>