<drac2>
def to_void(price):
	return round((price * 0.75), 2)

def get_crafting_cost(me, item, is_guild):
	cost = item.cost * 0.5

	if is_magic_item_adept(me, item):
		cost *= 0.5
	if is_guild:
		cost *= cost * 0.75

	return round(cost, 2)

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
		"thresholds": {15: 1, 21: 2, 26: 3},
		"xp": 30
	}
	magic_data = {
		"Common": {"actions": 7, "price": 100, "ss": 1, "ss_art": 1},
		"Uncommon": {"actions": 15, "price": 200, "ss": 3, "ss_art": 2},
		"Rare": {"actions": 40, "price": 1000, "ss": 5, "ss_art": 3},
		"Very Rare": {"actions": 120, "price": 2000, "ss": 6, "ss_art": 4},
		"Legendary": {"actions": 300, "price": 20000, "ss": 9, "ss_art": 5}
	}

	return item | magic_item | magic_data[item.rarity]

def init_mundane_item(item):
	mundane_item = {
		"thresholds": {10: 1, 16: 2, 21: 3},
		"xp": 15,
		"actions": ceil(item.price / 10)
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

def find_ss(me, min_level):
	for slot_level in range(min_level, 9):
		if me.spellbook.get_slots(slot_level) > 0:
			return slot_level
	return 0

def get_reward(crafting_context, my_roll):
	my_reward = 0

	for threshold, reward in crafting_context['thresholds'].items():
		if my_roll.total >= threshold:
			my_reward = max(my_reward, reward)

	return my_reward

def is_magic_item_adept(me, item):
	json = get("magic_item_adept_tiers")
	adept_tiers = load_json(json) if json else ["Common", "Uncommon"]

	return item.rarity in adept_tiers and me.levels["Artificer"] >= 10

def get_mod(me, item, args):
	stats = load_json(get("stats"))
	mod = stats[item.tool].mod

	if item.category is "Magic":
		mod += me.skills.arcana.bonus
		mod += me.skills.arcana.prof * proficiencyBonus
	else:
		if "exp" in args or item.tool.lower() in get('eTools', '').lower():
			mod += proficiencyBonus * 2
		elif "prof" in args or item.tool.lower() in get('pTools', '').lower():
			mod += proficiencyBonus

	return mod

def log_xp(xp, message):
	entry = {get('Timestamp'): f" {xp} | {message})"}

	log = load_json(get('xplog', '{}'))
	log.update(entry)
	set_cvar('xplog', dump_json(log))

	mod_cc("Experience", xp)

	return entry

def craft(me, mod, context, args):
	my_roll = vroll(my_dice(args, mod, context.item.category))

	reward = get_reward(context, my_roll)
	if me.levels['Artificer']:
		reward *= 4

	me.mod_cc(context.name, reward)
	context.current_actions = me.get_cc(context.name)

	xp_gained = context.item.xp * me.level if reward else 0
	cost = get_crafting_cost(me, context.item, me.get("guild") or "guild" in args) if reward else 0

	product = None
	if me.get_cc(context.name) > context.current_actions:
		product = context.item

	return reward, xp_gained, cost, product, my_roll

def build_desc(me, my_roll, context, ss):
	desc = f"**{context.item.tool}:** {my_roll}\n\n" \
				  f"Your progress on crafting this is now __{context.current_actions}/{context.actions}__!\n"

	if context.item.category is "magic":
		desc += f"\nYou use a spell slot for crafting: {me.spellbook.slots_str(ss)}"

	return desc

def build_footer(xp, item, cost, xp_entry):
	footer = f"{'You failed crafting and gain no xp' if not xp else f'Gain {xp / level} * {level} = {xp} XP!'}\n" \
			 f"This item costs {cost} GP to make and sells to players for {price} GP and to the void for {to_void(price)} GP!" \
			 f"You now have {get_cc('Experience')} XP and your most recent xplog entry will be:\n" \
			 f"{xp_entry}"
	return footer

def create_context(me, item):
	context_name = f"Crafting: {item.name}"

	# makes counter if it doesn't already exist
	me.create_cc_nx(context_name, 0, item.actions, None, None, 0)
	if me.get_cc(context_name) is item.actions or item.price is 0:
		me.set_cc(context_name, 0)

	context = {
		"name": context_name,
		"item": item,
		"current_actions": me.get_cc(context_name),
	}

	return context

def find_contexts(chosen_name, me, args):
	return []

def err_no_find(chosen_name):
	title = f"Couldn't find any items that match: {chosen_name}\n"
	return title, "", ""

def err_many_find(chosen_name, contexts):
	title = f"Found too many items that match: {chosen_name}\n"
	desc = ""
	for context in contexts:
		desc += f"{context['name']}\n"
	return title, desc, ""

def err_no_ss(item, ss_needed):
	title = f"{name} does not have a high enough level Spellslot\n"
	desc = f"You need at least one level {ss_needed} Spellslot available to craft {item.name}"
	return title, desc, ""

def search_name(chosen_name, me, args):
	contexts = find_contexts(chosen_name, me, args)
	if len(contexts) is 1:
		return contexts, None

	possibles = load_items(chosen_name)
	if not contexts and len(possibles) is 1:
		return [create_context(possibles.pop(), me)], None

	return contexts, possibles

def main(args):
	if len(args) < 1:
		err("oi")

	chosen_name = args[1]
	args = args[2:]
	me = character()

	contexts, possibles = search_name(chosen_name, me, args)

	if len(contexts) is not 1:
		if not contexts and not possibles:
			return err_no_find(chosen_name)
		else:
			return err_many_find(chosen_name, [context.item.name for context in contexts] + possibles)

	context = contexts.pop()
	item = context.item
	mod = get_mod(me, item, args)
	ss = 0

	if item.category is "Magic":
		ss_needed = item.ss_art if me.levels["Artificer"] else item.ss
		ss = find_ss(me, ss_needed)
		if not ss:
			return err_no_ss(item, ss_needed)

		me.spellbook.use_slot(ss)

	reward, xp, cost, product, my_roll = craft(me, mod, context, args)

	xp_entry = log_xp(xp, f"{context.name} ({context.current_actions}/{context.actions})")

	title = f'{me.name} does the crafting downtime for {item.name}'
	desc = build_desc(me, my_roll, context, ss)
	footer = build_footer(context, xp, item, cost, xp_entry)

	return title, desc, footer

</drac2>

{{title, desc, footer = main(&ARGS&)}}

-title "{{title}}"
-desc "{{desc}}"
-footer "{{footer}}

Made by Omie < 3"
-color <color>
-thumb <image>
