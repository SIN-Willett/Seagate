<drac2>
# gvar 608a7559-b0f5-4dbf-95d7-b4ce9ffd7cae
# THIS IS A TEST
args = &&&
listy = load_json(get_gvar("42ca55a5-199c-42e9-b89b-2f903a626b02"))

if len(args) > 3 or len(args) == 1:
    err("You've forgotten a few things here")
if len(args) == 2:
    err("Don't forget to add how many hours you are studying " + args[0])
if not args[2].isnumeric():
    err(args[2] + " is not a valid amount of hours to study")

learning = args[1].lower()
study_hours = int(args[2])

possibilities = [(topics, hours) for (topics, hours) in listy.items() if learning in topics.lower()]
if not possibilities:
    err(args[1] + " isn't a valid thing to study")
study = possibilities[0][0]
max_hours = possibilities [0][1]

character().create_cc_nx(study,0,max_hours,None,0)

title = f' tests the study downtime for {study}'
response = f"If this wasn't a test after studying for **{study_hours}** hours your current progress on studying __{study}__ would now be **{study_hours}/{max_hours}**!"
xplog_response = f"This is a test"
</drac2>
-title "{{name}}{{title}}"
-desc "{{response}}"
-footer "
{{xplog_response}}

Made by Omie <3"
-color <color>
-thumb <image>