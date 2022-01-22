# Gvar da0f7936-97bd-472c-b3fd-f72622df20e4
<drac2>
if not get("stats"):
    err("Stats not set")
args = &ARGS&
downtime_name = str(args[0])
if not args[1].isnumeric():
    err(args[1] + " is not a valid DC for " + args [0])

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
        
        if potential_mod > best_mod:
            best_mod = potential_mod
            best_option = option
            
    checks.append(best_option)
    mods.append(best_mod)

num_checks = len(mods)
dc = int(args[1])

if (num_checks == 3 and dc not in [10, 15, 20, 25]) or (num_checks == 2 and dc not in [10, 15, 20]):
    err("" + dc + " is not a valid DC for" + downtime_name)

rolls = []
successes = 0
tool = 0
    
# roll
for i in range(num_checks):
    if "adv" in args or "adv" + (i + 1) in args:
        rolls.append(vroll(f"2d20kh1+{mods[i]}"))
    elif "dis" in args or "dis" + (i + 1) in args:
        rolls.append(vroll(f"2d20kl1+{mods[i]}"))
    else:
        rolls.append(vroll(f"1d20+{mods[i]}"))

successes = sum(roll.total >= dc for roll in rolls)
if sum(roll.result.crit == 1 for roll in rolls) > 0:
    successes = num_checks

# respond
responses = load_json(get_gvar("2764f057-457a-483d-bb70-591863c8f695"))["illegal" if (num_checks == 3) else "legal"]
if num_checks == 3 and  successes == 0:
    response = f"You are now wanted for a DC {vroll(f'{dc}+5').total} crime! Ping a moderator, and let an admin know to add you to the wanted board."
else:
    response = responses[successes]

output_text = '\n'
for i in range(num_checks):
    success = 'Success!' if rolls[i].total >= dc else 'Failure!'
    output_text += '**' + checks[i] + ': **' + rolls[i] + '** ' + success + '**\n'
if "guid" in args:
    output_text += '**' + "Guidance" + ': **' + vroll(f'1d4') + ' add this to one of the above rolls!' + '\n'
</drac2>

-title "{{name}} does the {{downtime_name}} downtime!"
-desc "**DC:** {dc} {{output_text}}"
-footer "{{response}}
Made by Omen & Sin"
-color <color>
-thumb <image>