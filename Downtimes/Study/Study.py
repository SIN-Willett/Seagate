embed <drac2>
args = &ARGS&
listy = load_json(get_gvar("42ca55a5-199c-42e9-b89b-2f903a626b02"))

if len(args) > 2 or len(args) == 0:
    err("!help study")
if len(args) == 1:
    err("Don't forget to add how many hours you are studying " + args[0])
if not args[1].isnumeric():
    err(args[1] + " is not a valid amount of hours to study")

learning = args[0].lower()
study_hours = int(args[1])

possibilities = [(topics, hours) for (topics, hours) in listy.items() if learning in topics.lower()]
if not possibilities:
    err(args[0] + " isn't a valid thing to study")
study = possibilities[0][0]
max_hours = possibilities [0][1]

character().create_cc_nx(study,0,max_hours,None,0)
if get_cc(study) == max_hours:
    character().set_cc(study, 0)

character().mod_cc(study, +study_hours)

title = f' does the study downtime for {study}'
response = f"After studying for **{study_hours}** hours your current progress on studying __{study}__ is now **{character().get_cc(study)}/{max_hours}**!"
</drac2>
-title "{{name}} {{title}}"
-desc "{{response}}"
-footer "Made by Omie <3"
-color <color>
-thumb <image>