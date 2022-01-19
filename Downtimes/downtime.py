embed <drac2>
args = &ARGS&
downtime_name = str(args[0])
dc = int(args[1])
proficiency = "prof" in args
expertise = "exp" in args

# load data
all_downtimes = load_json(get_gvar("0d55e007-c9c3-43c8-b5b3-051353ed8797"))
our_downtime = all_downtimes[downtime_name]

stats = {
    "Dice set":               {"is_tool": True, "mod":charismaMod},
    "Playing card set":       {"is_tool": True, "mod":charismaMod},
    "Bagpipes":               {"is_tool": True, "mod":charismaMod},
    "Drum":                   {"is_tool": True, "mod":charismaMod},
    "Dulcimer":               {"is_tool": True, "mod":charismaMod},
    "Lute":                   {"is_tool": True, "mod":charismaMod},
    "Flute":                  {"is_tool": True, "mod":charismaMod},
    "Lyre":                   {"is_tool": True, "mod":charismaMod},
    "Horn":                   {"is_tool": True, "mod":charismaMod},
    "Pan flute":              {"is_tool": True, "mod":charismaMod},
    "Shawm":                  {"is_tool": True, "mod":charismaMod},
    "Viol":                   {"is_tool": True, "mod":charismaMod},
    "Cobbler's tools":        {"is_tool": True, "mod":dexterityMod},
    "Disguise Kit":           {"is_tool": True, "mod":dexterityMod},
    "Glassblower's tools":    {"is_tool": True, "mod":dexterityMod},
    "Jeweler's tools":        {"is_tool": True, "mod":dexterityMod},
    "Potter's tools":         {"is_tool": True, "mod":dexterityMod},
    "Tinker's tools":         {"is_tool": True, "mod":dexterityMod},
    "Thieves' tools":         {"is_tool": True, "mod":dexterityMod},
    "Weaver's tools":         {"is_tool": True, "mod":dexterityMod},
    "Woodcarver's tools":     {"is_tool": True, "mod":dexterityMod},
    "Alchemist's supplies":   {"is_tool": True, "mod":intelligenceMod},
    "Calligrapher's supplies":{"is_tool": True, "mod":intelligenceMod},
    "Cartographer's tools":   {"is_tool": True, "mod":intelligenceMod},
    "Poisoner's Kit":         {"is_tool": True, "mod":intelligenceMod},
    "Carpenter's tools":      {"is_tool": True, "mod":strengthMod},
    "Leatherworker's tools":  {"is_tool": True, "mod":strengthMod},
    "Mason's tools":          {"is_tool": True, "mod":strengthMod},
    "Smith's tools":          {"is_tool": True, "mod":strengthMod},
    "Land Vehicles":          {"is_tool": True, "mod":strengthMod},
    "Water Vehicles":         {"is_tool": True, "mod":strengthMod},
    "Brewer's supplies":      {"is_tool": True, "mod":wisdomMod},
    "Cook's utensils":        {"is_tool": True, "mod":wisdomMod},
    "Herbalism Kit":          {"is_tool": True, "mod":wisdomMod},
    "Painter's supplies":     {"is_tool": True, "mod":wisdomMod},
    "Navigator's tools":      {"is_tool": True, "mod":wisdomMod},
    "Performance":            {"is_tool": False, "mod":character().skills.performance.value},
    "History":                {"is_tool": False, "mod":character().skills.history.value},
    "Persuasion":             {"is_tool": False, "mod":character().skills.persuasion.value},
    "Arcana":                 {"is_tool": False, "mod":character().skills.arcana.value},
    "Athletics":              {"is_tool": False, "mod":character().skills.athletics.value},
    "Investigation":          {"is_tool": False, "mod":character().skills.investigation.value},
    "Acrobatics":             {"is_tool": False, "mod":character().skills.acrobatics.value},
    "Animal Handling":        {"is_tool": False, "mod":character().skills.animalHandling.value},
    "Perception":             {"is_tool": False, "mod":character().skills.perception.value},
    "Nature":                 {"is_tool": False, "mod":character().skills.nature.value},
    "Sleight of Hand":        {"is_tool": False, "mod":character().skills.sleightOfHand.value},
    "Survival":               {"is_tool": False, "mod":character().skills.survival.value},
    "Stealth":                {"is_tool": False, "mod":character().skills.stealth.value},
    "Medicine":               {"is_tool": False, "mod":character().skills.medicine.value},
    "Insight":                {"is_tool": False, "mod":character().skills.insight.value},
    "Religion":               {"is_tool": False, "mod":character().skills.religion.value},
    "Deception":              {"is_tool": False, "mod":character().skills.deception.value},
    "Intimidation":           {"is_tool": False, "mod":character().skills.intimidation.value}
}
 
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

</drac2>
-title "{{name}} does the {{downtime_name}} downtime!"
<drac2>
output_text = '\n'
for i in range(num_checks):
    success = 'Success!' if rolls[i].total >= dc else 'Failure!'
    output_text += '**' + checks[i] + ': **' + rolls[i] + '** ' + success + '**\n'
if "guid" in args:
    output_text += '**' + "Guidance" + ': **' + vroll(f'1d4') + ' add this to one of the above rolls!' + '\n'
</drac2>
-desc "**DC:** {dc} {{output_text}}"
-footer "{{response}}
Made by Omen & Sin"
-color <color>
-thumb <image>