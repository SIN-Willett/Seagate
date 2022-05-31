tembed <drac2>
# Code for !module
main_path = "3e98296d-6cca-4422-b414-735349e9f9f0"

# register of installed libraries
libs = load_yaml(get_gvar(get("import_path", "6b06857b-15d4-469e-a4d4-1c7e2915b1d9")))

# libs we've already imported
imported = ['avrae']

# allows print to work
stdembed = get_gvar("5c8267a0-ff5f-4468-bd96-53e0567b9c67")

def compile_file(filepath):
  """load a drac containing gvar, if it has import lines add them to the final code"""
  main = get_gvar(filepath)
  for line in main.splitlines():
    if not line:
      continue
    if "drac2>" in line:
      break
    parts = line.split(' ', 2)
    cmd, module_name = parts[0], parts[1]
    if cmd != "from" and cmd != "import":
      continue

    if module_name in imported:
      continue

    if module_name in libs:
      gvar = libs.pop(module_name)
      imported.append(module_name)
      main = main.replace(line, compile_file(gvar))
    else:
      err(f'''Could not import module : "{module_name}"''')
  return main

# the final product
return compile_file(main_path).replace("&&&", "&ARGS&").replace("&STDEMBED&", stdembed)
</drac2>