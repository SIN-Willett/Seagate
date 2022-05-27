embed <drac2>
args = &ARGS&

locations = load_json(get_gvar("02762117-db82-416b-95cb-4a9f0eddd585"))
input_channel = args[0]

if not locations[input_channel]:
    err(" " + input_channel + "information does not exist in our database")

location = locations[input_channel].location
location_type = locations[input_channel].location_type 
location_image = locations[input_channel].location_image
about = locations[input_channel].about
map_image = locations[input_channel].map_image
size = locations[input_channel].size

response = "" + input_channel + "\n\n" + about
if not map_image == 0:
    if not"short" in args:
        response += "\n```!map -attach MAP -options d -mapsize " + size + " -bg " + map_image + "```\n[Click here to see the map](" + map_image + ")"
</drac2>
-title "__{{location}}__ is a {{location_type}}!"
-desc "{{response}}"
-footer "Made by Omie <3"
-color <color>
-thumb <location_image>