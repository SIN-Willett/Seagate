embed <drac2>
args = &ARGS&

npcs = load_json(get_gvar("ad013e74-682c-4866-a567-d3cb28c7f14c"))
input_npc = args[0]

chosen_npc = None
for key in npcs:
    if input_npc.lower() in key.lower():
            chosen_npc = key
            break
    if chosen_npc:
        break

if not chosen_npc:
    err(" " + input_npc + "information does not exist in our database")

npc_name    = chosen_npc
npc_title   = npcs[chosen_npc].npc_title
race        = npcs[chosen_npc].race
npc_class   = npcs[chosen_npc].npc_class
pronouns    = npcs[chosen_npc].pronouns
location    = npcs[chosen_npc].location
image       = npcs[chosen_npc].image
quote       = npcs[chosen_npc].quote

response = "They are a " + race + npc_class + " and use the pronouns " + pronouns + ".\n\nCan be found at " + location + "\n```" + quote + "```"

</drac2>
-title "__{{npc_name}}__ is {{npc_title}}!"
-desc "{{response}}"
-footer "Made by Omie <3"
-color <color>
-thumb <image>