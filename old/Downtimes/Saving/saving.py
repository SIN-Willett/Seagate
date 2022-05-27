<drac2>
args = &&&
pars = argparse(args).last
save_name = args [1]
downtime_name = args[2]
downtime_args = args[2:]

dt_option = load_json(get_gvar("3b5d0b01-08fb-439b-9f6b-94def1f241a4"))
saving_dt = downtime_name in dt_option

if not save_name.isnumeric():
    err("Downtimes can only be saved to numbers, it's important, trust me.")
if not saving_dt:
    err("This downtime does not exist")

dt_save = {save_name : downtime_args}

dt_saved = get("DTsaved")
if not dt_saved:
    character().set_cvar("DTsaved", dump_json(dt_save))
else:
    dt_saved = load_json(get("DTsaved"))
    dt_saved[save_name] = downtime_args
    character().set_cvar("DTsaved", dump_json(dt_saved))
</drac2>
-title "{{name}} has saved a Downtime!"
-desc "**Save {{save_name}}:** {{downtime_args}}."
-footer "Made by Omie <3"
-color <color>
-thumb <image>