<drac2>
def to_void_price(price):
    return round((price * 0.75), 2)

def sale_message(cost, price):
    return f"This item costs {cost} GP to make and sells to players for {price} GP and to the void for {to_void_price(price)} GP!" if price else None

def xp_message(xp):
    return "You failed crafting and gain no xp" if not xp else f"Gain {xp / level} * {level} = {xp} XP!"

def fuzzy_get(dictionary, key_to_get):
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

def my_dice(args, my_mod, craft_type):
    pars = argparse(args).last
    mydice = ""
    if "adv" in args:
        mydice += f"2d20kh1+{my_mod}"
    elif "dis" in args:
        mydice += f"2d20kl1+{my_mod}"
    else:
        mydice += f"1d20+{my_mod}"

    if "guid" in args:
        mydice += "+1d4[guidance]"
    if "ls" in args and craft_type is "Mundane":
        mydice += "+1[luckstone]"
    if "-b" in args or "-bonus" in args:
        bonus = argparse(args).last("b") or argparse(args).last("bonus") or ""
        mydice += f"+{bonus}{[bonus]}"
    return mydice

def find_ss(the_character, min_level):
    for slot_level in range(min_level, 9):
        if the_character.spellbook.get_slots(slot_level) > 0:
            return slot_level
    return 0

def get_reward(crafting_context, my_roll):
    my_reward = 0

    for threshold, reward in crafting_context['thresholds'].items():
        if my_roll.total >= threshold:
            my_reward = max(my_reward, reward)

    return my_reward

def load_artificer(context, item, artificer_level):
    item.ss = item.ss_art

    json = get("magic_item_adept_tiers")
    adept_tiers = load_json(json) if json else ["Common", "Uncommon"]

    if item.rarity in adept_tiers and artificer_level >= 10:
        context["magic_item_adept"] = True

    context["artificer_level"] = artificer_level

    for roll in context["thresholds"]:
        context["thresholds"][roll] *= 4

def load_magic(context, item, args):
    artificer_level = character().levels["Artificer"]
    if artificer_level:
        load_artificer(context, item, artificer_level)

    arcana = character().skills.arcana.bonus + (character().skills.arcana.prof * proficiencyBonus)
    context["mod"] += int(arcana)

    ss = find_ss(character(), item.ss)
    if not ss:
        err("You do not have enough spell slots remaining")

    context["magic"] = ss

def load_mundane(context, item, args):
    if "exp" in args or item.tool.lower() in get('eTools','').lower():
        context.mod += proficiencyBonus * 2
    elif "prof" in args or item.tool.lower() in get('pTools','').lower():
        context.mod += proficiencyBonus

def get_crafting_context(item, args):
    stats = load_json(get("stats"))
    context_name = f"Crafting: {item.name}"

    # makes counter if it doesn't already exist
    character().create_cc_nx(context_name, 0, item.actions, None, None, 0)
    if character().get_cc(context_name) is item.actions or item.price is 0:
        character().set_cc(context_name, 0)

    context = {
        "name": context_name,
        "item": item,
        "mod": stats[item.tool].mod,
        "current_actions": character().get_cc(context_name),
        "guild": get("Guild") or "guild" in args
    }

    if item.category is "Magic":
        load_magic(context, item, args)
    else:
        load_mundane(context, item, args)

    # context = context | {arg: True for arg in args}
    return context

def log_xp(xp_gained, message):
    xplog = load_json(get('xplog','{}'))

    entry = {
        get('Timestamp'): f" {xp_gained} | {message})"
    }

    xplog.update(entry)

    set_cvar('xplog', dump_json(xplog))
    mod_cc("Experience", xp_gained)

    return entry

def log_crafting_xp(crafting_context, xp_gained):
    return log_xp(xp_gained, f"{crafting_context['name']} ({crafting_context['current_actions']}/{crafting_context['actions']})")

def craft(crafting_context, item):
    if item.category is "Magic":
        character().spellbook.use_slot(crafting_context["magic"]["ss"])

    myroll = vroll(my_dice(args, crafting_context["mod"], crafting_context["category"]))

    reward = get_reward(crafting_context, myroll)

    character().mod_cc(crafting_context["name"], reward)

    xp_gained = crafting_context["xp"] * character().level if reward else 0

    cost = item["cost"] * 0.5 if reward else 0

    if "magic_item_adept" in crafting_context:
        cost *= 0.5

    if "guild" in crafting_context:
        cost *= cost * 0.75

    cost = round(cost, 2)

    return reward, cost, xp_gained

def build_description(crafting_details, my_roll, current_actions, actions):
    description = f"**{crafting_details.tool}:** {my_roll}\n\n" \
                  f"Your progress on crafting this is now __{current_actions}/{actions}__!\n"

    if crafting_details.category is "Magic":
        description += magic_response

    return description

def build_footer(crafting_context, xp, item, cost, xp_entry):
    footer = f"{xp_message(xp)}\n" \
             f"{sale_message(cost, item['price'])}" \
             f"You now have {get_cc('Experience')} XP and your most recent xplog entry will be:\n" \
             f"{xp_entry}"

    if item.category is "magic":
            footer += f"\nYou use a spell slot for crafting: {character().spellbook.slots_str(crafting_context['magic'])}"

    return footer

def main(args):
    if len(args) < 1:
        err("oi")

    craftables = load_json(get_gvar("c28ac8be-d70e-4842-8f5c-b9e251ce4eb6"))

    possibles = find_craftables_by_name(args[1], craftables)
    if not possibles:
        err("You have failed to select a craftable, please check the name of the item you want to craft against the crafting spreadsheet <3")

    if len(possibles) > 1:
        err_msg = "You selected an ambiguous craftable, try again with:\n"
        for craftable in possibles:
            err_msg += f"{craftable.name}\n"
        err(err_msg)

    item = load_unknowns(possibles.pop())

    crafting_context = get_crafting_context(item, args[2:])

    reward, cost, xp = craft(crafting_context, item)

    xp_entry = log_crafting_xp(crafting_context, xp)

    title = f'{character().name} does the crafting downtime for {item.name}'
    description = build_description(item, crafting_result.roll, crafting_context['current_actions'], crafting_context['actions'])
    footer = build_footer(crafting_context, xp, item, cost, xp_entry)

    return title, description, footer

def create_context(me, item):
    stats = load_json(get("stats"))
    context_name = f"Crafting: {item.name}"

    # makes counter if it doesn't already exist
    character().create_cc_nx(context_name, 0, item.actions, None, None, 0)
    if character().get_cc(context_name) is item.actions or item.price is 0:
        character().set_cc(context_name, 0)

    context = {
        "name": context_name,
        "item": item,
        "mod": stats[item.tool].mod,
        "current_actions": me.get_cc(context_name),
        "guild": get("Guild") or "guild" in args
    }

    if item.category is "Magic":
        load_magic(context, item, args)
    else:
        load_mundane(context, item, args)

    return context

def find_contexts(chosen_name, me, args):
    return []

def work_on_craft(context, me):

    pass

def err_no_find(chosen_name):
    title = f"Could not find an item called {chosen_name}"
    return title, "", ""

def err_many_find(chosen_name, contexts):
    title = f"Found too many items that match: {chosen_name}\n"
    description = ""
    for context in contexts:
        description += f"{context['name']}\n"
    return title, description, ""

def search_name(chosen_name, me):
    contexts = find_contexts(chosen_name, me, args)
    if len(contexts) is 1:
        return contexts, None

    possibles = load_items(chosen_name)
    if not contexts and len(possibles) is 1:
        return [create_context(possibles.pop(), me)], None

    return contexts, possibles

def crafting_dt(chosen_name, me, args):
    contexts, possibles = search_name(chosen_name, me)

    if len(contexts) is not 1:
        if not contexts and not possibles:
            return err_no_find(chosen_name)
        else:
            return err_many_find(chosen_name, [context.item.name for context in contexts] + possibles)

    context = contexts.pop()

    xp, xp_entry, item = work_on_craft(context, me)

    if item:
        return craft_completed()
    elif xp:
        return craft_progressed()
    else:
        return crafting_failed()

    xp_entry = log_crafting_xp(context, xp)
    title = f'{character().name} does the crafting downtime for {item.name}'
    description = build_description(item, crafting_result.roll, crafting_context['current_actions'], crafting_context['actions'])
    footer = build_footer(crafting_context, xp, item, cost, xp_entry)

    return title, description, footer

def main(args):
    if len(args) < 1:
        err("oi")

    chosen_name = args[1]
    args = args[2:]
    me = character()

    return crafting_dt(chosen_name, me, args)
</drac2>

{{title, description, footer = main(&&&)}}

-title "{{title}}"
-desc "{{description}}"
-footer "{{footer}}

Made by Omie <3"
-color <color>
-thumb <image>
