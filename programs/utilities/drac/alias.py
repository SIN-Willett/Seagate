tembed <drac2>

main = get_gvar("f6ee7dcf-764d-43e2-97ce-52dadaf266dc")

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

return main.replace("&&&", "&ARGS&").replace("&STDEMBED&", stdembed)
</drac2>