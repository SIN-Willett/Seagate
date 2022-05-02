<drac2>
# Gvar da0f7936-97bd-472c-b3fd-f72622df20e4
if not get("stats"):
    err("Stats not set")
args = &&&
downtime_name = str(args[0])
if not args[1].isnumeric():
    err(f"{args[1]} is not a valid DC for {args [0]}")

proficiency = "prof" in args
expertise = "exp" in args

# load data
all_downtimes = load_json(get_gvar("0d55e007-c9c3-43c8-b5b3-051353ed8797"))
our_downtime = all_downtimes[downtime_name]

stats = load_json(get("stats"))
 
mods = []
checks = []

tool_mod = 0
e_tools = get('eTools','').lower()
p_tools = get('pTools','').lower()
        
#choose best
for check in our_downtime:
    best_mod = 0
    best_option = None
    for option in check:
        potential_mod = stats[option].mod
        
        proficiency = (stats[option].is_tool and "prof" in args) or option.lower() in p_tools
        expertise = (stats[option].is_tool and "exp" in args) or option.lower() in e_tools
        
        if (stats[option].is_tool or expertise or proficiency) and "ls" in args:
            potential_mod += 1
        if expertise:
            potential_mod += ((proficiencyBonus) * 2)
        elif proficiency:
            potential_mod += (proficiencyBonus)
        
        if potential_mod > best_mod or best_mod == 0:
            best_mod = potential_mod
            best_option = option
            
    checks.append(best_option)
    mods.append(best_mod)

num_checks = len(mods)
dc = int(args[1])

if (num_checks == 3 and dc not in range(10, 26, 5)) or (num_checks == 2 and dc not in range(10, 21, 5)):
    err("" + dc + " is not a valid DC for" + downtime_name)

rolls = []
num_successes = 0
tool = 0

arg_space = args + ' '
pars = argparse(arg_space).last

# roll
for i in range(num_checks):
    if f"-b{i + 1}" in args or f"-bonus{i + 1}" in args:
        bonus = pars(f"b{i + 1}", None, int) or pars(f"bonus{i + 1}", None, int) or 0
        mods[i] = mods[i] + bonus

    if "-b" in args or "-bonus"  in args:
        bonus = pars("b", None, int) or pars("bonus", None, int) or 0
        mods[i] = mods[i] + bonus

    if "adv" in args or "adv" + (i + 1) in args:
        rolls.append(vroll(f"2d20kh1+{mods[i]}"))
    elif "dis" in args or "dis" + (i + 1) in args:
        rolls.append(vroll(f"2d20kl1+{mods[i]}"))
    else:
        rolls.append(vroll(f"1d20+{mods[i]}"))

roll_values = [roll.total for roll in rolls]

guid_index = -1
guid_value = 0
if "guid" in args:
    losses = [roll.total for roll in rolls if roll.total < dc]
    if not losses:
        best = max(roll_values)
    else:
        best = max(losses)

    index = roll_values.index(best)
    guid_roll = vroll("+1d4[guidance]")
    guid_index = index
    guid_value = guid_roll.total

successes = [rolls[i].total + (guid_value if i == guid_index else 0) >= dc for i in range(num_checks)]
num_successes = sum(successes)
if sum(roll.result.crit == 1 for roll in rolls) > 0:
    num_successes = num_checks
    successes = [True for i in range(num_checks)]

# response
output_text = ""
for i in range(num_checks):
    tab = '‎ ' * ((len(checks[i]) * 2) + 2)
    guidybuidy = f"""
    {tab}{str(guid_roll).split(" =", 1)[0]} = `{(rolls[i].total + guid_value)}`""" if (i == guid_index) else ""
    output_text += f"""
    **{checks[i]}:** {rolls[i]}{guidybuidy} **{'Success!' if successes[i] else 'Failure!'}**"""

crime = (num_checks == 3)
strdc = str(dc)
data = load_json(get_gvar("cd374b66-bf6e-4ef9-ac64-d9e213a5c0cb"))["illegal" if crime else "legal"]

xp = data[strdc]["XP"]
gp = data[strdc]["Gold"]
total_xp = 0
total_earned = gp
response = ""
if crime:
    if not num_successes:
        response = f"You are now wanted for a DC {vroll(f'{dc}+5').total} crime! Ping a moderator, and let an admin know to add you to the wanted board."
        total_earned = 0
        xp = 0
    if num_successes == 1:
        response = f"You are now wanted for your crimes! Ping a moderator, and let an admin know to add you to the wanted board."
        total_earned = 0
        xp = 0
    if num_successes == 2:
        total_earned = (gp * 0.5)
        xp = int(xp * 0.5)
        total_xp = xp * level
        response = f"You earn {xp} * {level} = {total_xp} XP and "
    else:
        total_xp = xp * level
        response = f"You earn {xp} * {level} = {total_xp} XP and "
else:
    if not num_successes:
        response = f"You earn no GP and no experience."
        total_earned = 0
        xp = 0
    if num_successes == 1:
        total_earned = (gp * 0.5)
        xp = int(xp * 0.5)
        total_xp = xp * level
        response = f"You earn {xp} * {level} = {total_xp} XP and "
    else:
        total_xp = xp * level
        response = f"You earn {xp} * {level} = {total_xp} XP and "

gp_gained = floor(total_earned)
sp_gained = floor((total_earned - gp_gained) * 10)
cp_gained = int((((total_earned - gp_gained) * 10) - sp_gained) * 10)

bags = load_json(get("bags"))
i = 0
for bag in bags:
    if bag[0] == "Coin Pouch":
        break
    i = i + 1

if i == len(bags):
    err("you have no coin pouch")

bags[i][1]['cp'] = int(bags[i][1]['cp'] + cp_gained)
bags[i][1]['sp'] = int(bags[i][1]['sp'] + sp_gained)
bags[i][1]['gp'] = int(bags[i][1]['gp'] + gp_gained)

total_gp = bags[i][1].gp
total_sp = bags[i][1].sp
total_cp = bags[i][1].cp
character().set_cvar("bags", dump_json(bags))

coin_response = f"You now have "

if cp_gained != 0:
    response += f"{sp_gained} SP and {cp_gained} CP!"
    coin_response += f"{total_sp} SP and {total_cp} CP!"
elif sp_gained != 0:
    response += f"{gp_gained} GP and {sp_gained} SP!"
    coin_response += f"{total_gp} GP and {total_sp} SP!"
else:
    response += f"{gp_gained} GP!"
    coin_response += f"{total_gp} GP!"

char_xp = get_cc(exp_cc)

def log_xp(xp_gained, message):
    xplog = load_json(get('xplog','{}'))

    entry = {
        get('Timestamp'): f" {xp_gained} | {message})"
    }

    xplog.update(entry)

    set_cvar('xplog', dump_json(xplog))
    mod_cc("Experience", xp_gained)

    return entry

def log_main_xp(main_context, xp_gained):
    return log_xp(xp_gained, f"{total_xp} | DC {main_context['dc']}  {main_context['name']} downtime")

def build_description(dc, num_checks, checks, guid_roll, rolls, guid_value, guid_index, successes):
    tab = '‎ ' * ((len(checks[i]) * 2) + 2)
    for i in range(num_checks):
        guidybuidy = f"\n{tab}{str(guid_roll).split(' =', 1)[0]} = `{(rolls[i].total + guid_value)}`""" if (i == guid_index) else ""
        description = f"**DC:** {dc} \n"\
                    f"**{checks[i]}:** {rolls[i]}{guidybuidy} **{'Success!' if successes[i] else 'Failure!'}**"
    
    return f"{description}"

def build_footer(coin_response, bagcoin_response, char_xp, timestamp, xp_args):
    footer = f"{coin_response}\n\n" \
            f"{bagcoin_response}\n\n" \
            f"You now have {char_xp} XP and your most recent xplog entry will be:\n" \
            f"{timestamp}: {xp_args}"
    return footer

def main(args):
    
    xp_entry = log_main_xp(main_context, xp)
    title = f"{character().name} does the {main_context['name']} downtime!"
    description = build_description(dc, num_checks, checks, guid_roll, rolls, guid_value, guid_index, successes)
    footer = build_footer(coin_response, bagcoin_response, char_xp, timestamp, xp_args)

    return title, description, footer

</drac2>

{{title, description, footer = main(&&&)}}

-title "{{title}}"
-desc "{{description}}"
-footer "{{footer}}

Made by Omen & Sin"
-color <color>
-thumb <image>
