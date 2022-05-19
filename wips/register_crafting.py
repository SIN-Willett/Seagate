embed
args = &ARGS&
<drac2>
character().set_cvar_nx("craft_register", {})
def to_void_price(price):
    return round((price * 0.75), 2)

def sale_message(cost, price):
    return f"This item costs {cost} GP to make and sells to players for {price} GP and to the void for {to_void_price(price)} GP!" if price else None

def fuzzy_get(dictionary, key_to_get):
    value = dictionary.get(key_to_get.lower(), None)
    if value:
        return [value]

    possibles = []
    for key, details in dictionary.items():
        if key_to_get.lower() in key:
            possibles.append(details)

    return possibles

    value = dictionary.get(key_to_get.lower(), None)
    if value:
        return [value]

    possibles = []
    for key, details in dictionary.items():
        if key_to_get.lower() in key:
            possibles.append(details)

    return possibles

def init_magic_item(item):
    magic_item = {
        "thresholds" : {15 : 1, 21 : 2, 26: 3},
        "xp" : 30
    }

    magic_data = {
        "Common"	:	{"actions": 7, "price": 100, "ss": 1, "ss_art": 1},
        "Uncommon"	:	{"actions": 15, "price": 200, "ss": 3, "ss_art": 2},
        "Rare"		:	{"actions": 40, "price": 1000, "ss": 5, "ss_art": 3},
        "Very Rare"	:	{"actions": 120, "price": 2000, "ss": 6, "ss_art": 4},
        "Legendary"	:	{"actions": 300, "price": 20000, "ss": 9, "ss_art": 5}
    }

    return item | magic_item | magic_data[item.rarity]

def init_mundane_item(item):
    mundane_item = {
        "thresholds" : {10 : 1, 16 : 2, 21: 3},
        "xp" : 15,
        "actions" : ceil(item.price / 10)
    }

    return item | mundane_item

def init_item(item):
    if item.category is "Magic":
        item = init_magic_item(item)
    else:
        item = init_mundane_item(item)

    # makes the minimum 1 action
    if item.actions < 1:
        item.actions = 1
    # makes the actions 3 for house related things
    if not item.price:
        item.actions = 3

    return item

def load_items(name):
    craftables = load_json(get_gvar("c28ac8be-d70e-4842-8f5c-b9e251ce4eb6"))
    possibles = fuzzy_get(craftables, name)
    return [init_item(item) for item in possibles]

def context(crafting):
    item = load_items(crafting)

    context = {
        item[0]: {
            "price": ??,
            "tool": ??,
            "actions": ??,
            "progress": ??,
            "cost": ??,
            "paid": ??,
            "magic": ??
            "thresholds":??
        }
    }
    return context

def register(crafting):
    craft_register = load_json(character().get("craft_register","{}"))
    craft_register.append(context(crafting))
    character().set_cvar("craft_register", dump_json(craft_register))

def paying(crafting, coin):
    craft_register = load_json(character().get("craft_register","{}"))
    do_coin(coin)
    craft_register[crafting]["paid"] = craft_register[crafting]["paid"] + coin
    character().set_cvar("craft_register", dump_json(craft_register))

def do_coin(coin):
    coins = character().coinpurse
    purse = coins.get_coins()
    if purse["total"] > coin:
        gp = floor(coin)
        sp = floor((coin - gp) * 10)
        cp = int((((coin - gp) * 10) - sp) * 10)
        coins.modify_coins(0, -gp, 0, -sp, -cp)
    else:
        err("You do not have enough coin")

def listing():
    craft_register = load_json(character().get("craft_register","{}"))
    print_list = "__**Name || ?/? actions || ?/? gp**__\n"
    for x in craft_register:
        print_list += f'{craft_register[x]["name"]} || {craft_register[x]["progress"]} / {craft_register[x]["actions"]} actions || {craft_register[x]["paid"]} / {craft_register[x]["cost"]} gp\n'
    return print_list

def main(args):
    if len(args) is 0:
        listing()
    elif args[0] in "listing":
        listing()
    elif args[0] in "register":
        register(args - args[0])
    elif args[0] in "paying":
        paying(args - args[0])
    else:
        err(f"What do you mean by {args}? Because it's nothing this alias knows what to do with.")

</drac2>

# !craft register ["sdibfhsd"]
# !craft pay [1/"sdibfhsd"] [coin]
# !craft list
# "Candle of the Deep" : {"name" : "Candle of the Deep", "price" : ??, "tool" : "Alchemig