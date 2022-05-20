# Gvar 535b9ea0-faa9-4aa1-a051-5a85a21be62e
<drac2>
args = &&&
pars = argparse(args).last

stats = load_json(get("stats"))
potential_check = ["Cook's Utensils", "Persuasion"]
best_option = ""
best_mod = 0
e_tools = get('eTools','').lower()
p_tools = get('pTools','').lower()

for option in potential_check:
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

mydice = ""
if "adv" in args:
    mydice += f"2d20kh1+{best_mod}"
elif "dis" in args:
    mydice += f"2d20kl1+{best_mod}"
else:
    mydice += f"1d20+{best_mod}"
if "guid" in args:
    mydice += "+1d4[guidance]"
if "-b" in args or "-bonus" in args:
    bonus = pars("b", pars("bonus",""))
    mydice += (f"+{bonus}[bonus]")

myroll = vroll(mydice)

title = f" does the Soup Kitchen Volunteering downtime"
output_text = f"** {best_option}: ** {myroll}\n"

xp_table = load_json(get_gvar("1735dc7f-fedd-4d83-8a37-584ca6c55d02"))

exp_cc = "Experience"
level = level
next_level = level + 1
message = ""

if level < 20:
    if character().get_cc(exp_cc) >= xp_table[str(next_level)]:
        message = f"\nYou have leveled up to {next_level}!"
        level = next_level

response = ""
xp = 0
total_xp = 0 
if myroll.result.total <= 10:
    response = "You are thanked for your efforts and receive a hug from Lo."
elif myroll.result.total <= 15:
    response = "You receive 10 goodberries as thanks for your efforts."
elif myroll.result.total <= 20:
    xp = 15
    total_xp = xp * level
    response = "You are granted the effects of the 'Enhance Ability' spell (one ability of your choice) for 24 hours."
else:
    xp = 30
    total_xp = xp * level
    response = "You are granted the effects of the Guidance cantrip for 24 hours."


xp_args = f"{total_xp} | Soup Volunteer downtime (Roll: {myroll.result.total})"

xplog = load_json(get('xplog','{}'))
timestamp = get("Timestamp")
xplog.update({timestamp:xp_args})
character().set_cvar('xplog',dump_json(xplog))
character().mod_cc(exp_cc,total_xp)

char_xp = character().get_cc(exp_cc)

xplog_response = f"You gain {total_xp} XP and now have {char_xp} XP"

</drac2>
-title "{{name}} {{title}}"
-desc "{{output_text}}"
-footer "{{response}}

{{xplog_response}}{{message}}
Your most recent xplog entry will be:
{{timestamp}}: {{xp_args}}

Made by Omie <3"
-color <color>
-thumb <image>