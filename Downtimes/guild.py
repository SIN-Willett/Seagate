embed <drac2>
args = &ARGS& + [' ']
pars = argparse(args).last

guild_name = pars("name", pars("guild",""))
rank = pars("rank",0)
role = pars("role", pars("title",""))

possible_guilds = load_json(get_gvar("d97c7ed1-cde8-418f-898d-12387408cc6d"))
if guild_name:
    for possible in possible_guilds:
        if guild_name.lower() in possible.lower():
            guild_name = possible
    if not possible:
        err(guild_name + " is not a registered Guild")
        
data = {   "guild_name"  : guild_name,
            "rank"       : rank,
            "role"       : role
}

guild = get("Guild")
if not guild:
    character().set_cvar("Guild", dump_json(data))

guild = load_json(get("Guild"))
for key, value in data.items():
    if not value:
        data[key] = guild[key]

character().set_cvar("Guild", dump_json(data))
</drac2>
-title "{{name}} is a member of __{{data.guild_name}}__!"
-desc "This is a __Rank {{data.rank}}__ guild of which they are __{{data.role}}__."
-footer "Made by Omie <3"
-color <color>
-thumb <image>
