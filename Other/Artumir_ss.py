embed
<drac2>
args = &ARGS&
slots = load_json(get("slots","{}"))
t_response = ""
response = ""

if len(args) is 0:
    t_response = f"{name} checks their spell slots."
    for x in slots:
        if slots[x]["ss_max"] > 0:
            response += f"**Level {x}:** {slots[x]['ss_current']} / {slots[x]['ss_max']}\n"
else:
    if args[0].lower() in "lrest":
        t_response = f"{name} rests their spell slots."
        for x in slots:
            slots[x]["ss_current"] = slots[x]["ss_max"]
            if slots[x]["ss_max"] > 0:
                response += f"**Level {x}:** {slots[x]['ss_current']} / {slots[x]['ss_max']}\n"

    if args[0].isnumeric():
        ss = args[0]
        if slots[ss]["ss_current"] > 0:
            slots[ss]["ss_current"] = slots[ss]["ss_current"] - 1
            t_response = f"{name} casts a level {ss} spell!"
            response = f"**Level {ss}:** {slots[ss]['ss_current']}/{slots[ss]['ss_max']}"
        else:
            err(f"You did not have any level {ss} spell slots remaining.")

character().set_cvar("slots", dump_json(slots))

</drac2>
-title "{{t_response}}"
-desc "{{response}}"
-footer "Made by Omie <3"
-color <color>
-thumb <image>