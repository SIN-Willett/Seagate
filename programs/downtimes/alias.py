tembed <drac2>
args = &ARGS&
if not args:
  err(f"usage: {ctx.prefix}{ctx.alias} downtime [options]")

dt_name = args[0]

downtimes = load_yaml(get_gvar("c10b8da4-f2f3-4d0e-8673-ecc4755de1f3"))

main = get_gvar(downtimes[None])
if dt_name in downtimes:
  main = get_gvar(downtimes[dt_name])
  args = args[1:]

libs = load_yaml(get_gvar(get("import_path", "6b06857b-15d4-469e-a4d4-1c7e2915b1d9")))
stdembed = get_gvar("5c8267a0-ff5f-4468-bd96-53e0567b9c67")
IMPORT_PREFIX = "import "

for line in main.splitlines():
  if not line:
    continue
  if not line.startswith(IMPORT_PREFIX):
    break
  module_name = line.removeprefix(IMPORT_PREFIX)
  if module_name in libs:
    main = main.replace(line, get_gvar(libs[module_name]))
  else:
    err('''Could not import module : "{module_name}"''')

return main.replace("&&&", str(args)).replace("&STDEMBED&", stdembed)
</drac2>