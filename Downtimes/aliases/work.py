embed <drac2>
args = &ARGS& + [' ']
pars = argparse(args).last

location = pars("loc", pars("location",""))
income = pars("inc", pars("income", pars("wage",0)))
check = pars("check", pars("tool",""))
role = pars("role", pars("job",""))

check_option = load_json(get_gvar("ce2b12c8-ca0b-43bd-99c5-5d016bb8d415"))
if check:
    for possible in check_option:
        if check.lower() in possible.lower():
            check = possible
    if not possible:
        :("This check does not exist")

data = {   "location"   : location,
            "income"    : income,
            "check"     : check,
            "role"      : role
}

work = get("Work")
if not work:
    character().set_cvar("Work", dump_json(data))

work = load_json(get("Work"))
for key, value in data.items():
    if not value:
        data[key] = work[key]

character().set_cvar("Work", dump_json(data))
</drac2>
-title "{{name}} now works at __{{data.location}}__!"
-desc "Where they use __{{data.check}}__ to do work as __{{data.role}}__.
This earns them an income of **{{data.income}}** GP."
-footer "Made by Omie <3"
-color <color>
-thumb <image>