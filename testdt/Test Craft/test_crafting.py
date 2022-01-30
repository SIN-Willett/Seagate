<drac2>
# gvar 9f616ca4-939b-44d4-be89-e80f77e89c24
# THIS IS A TEST
args = &&&
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
        if (inputcraft.lower() in craftableName.lower()):
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
    
##cvar for tool to attribute matching
stats = load_json(get("stats"))
mod = stats[tool].mod
arcana = character().skills.arcana.bonus + (character().skills.arcana.prof * proficiencyBonus)
magic_response = None
        
artificer_level = 0
for (cls, level) in character().levels:
    if cls == "Artificer":
        if level > 1:
            artificer_level = level
            ss = ss_art
    break

if crafting_type == "Magic":
    mod += int(arcana)
    magic_response = f"If this wasn't a test you would use a level {ss} spell slot for crafting"
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
if crafting_type == "Mundane":
    if myroll.total < 10:
        xp = 0
    elif myroll.total < 16:
        xp = 15
    elif myroll.total < 21:
        xp = 15
    else:
        xp = 15
elif (artificer_level >= 10) and (magic_item_adept == True):
    if myroll.total < 15:
        xp = 0
        cost = (cost * 0.5)
    elif myroll.total < 21:
        xp = 30
        cost = (cost * 0.5)
    elif myroll.total < 26:
        xp = 30
        cost = (cost * 0.5)
    else:
        xp = 30
        cost = (cost * 0.5)     
else:
    if myroll.total < 15:
        xp = 0
    elif myroll.total < 21:
        xp = 30
    elif myroll.total < 26:
        xp = 30
    else:
        xp = 30

total_xp = xp * level

char_xp = get_cc("Experience")

xplog_response = f"You have {char_xp} XP"

title = f'{name} tests the crafting downtime for {item_name}'
response_xp = ()
if xp == 0:
    response_xp = f"You failed when testing crafting and gain no xp"
else:
    response_xp = f"If this wasn't a test you'd gain {xp} * {level} = {total_xp} XP!"
</drac2>
-title "{{title}}"
-desc "**{{tool}}:** {{myroll}}

__**You make no progress on crafting this as this is a test!**__
{{magic_response}}"
-footer "{{response_xp}}

This item costs {{round(cost, 2)}} GP to make and sells to players for {{price}} GP and to the void for {{sell}} GP!

{{xplog_response}}
THIS IS A TEST

Made by Omie <3"
-color <color>
-thumb <image>