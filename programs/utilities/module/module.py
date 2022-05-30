!gvar edit 3e98296d-6cca-4422-b414-735349e9f9f0
import files
import yaml

<drac2>
def main(args):
  path = get('import_path', '6b06857b-15d4-469e-a4d4-1c7e2915b1d9')
  libstring = get_gvar(path)
  if not args:
    print('Modules in current Environment', '', stdtitle)
    print(code_block(f'{ctx.prefix}gvar edit {path}\n\n{libstring}', 'yaml'))
    return None

  module_name = args[0]
  libs = load_yaml(libstring)

  if not module_name in libs:
    err(f'Could not find module called {module_name}')

  code_gvar = libs[module_name]
  code = get_gvar(code_gvar)

  print(code_block(f'{ctx.prefix}gvar edit {code_gvar}\n{code}', 'py'))
  print(f'Module {module_name}', '', stdtitle)

main(&&&)
</drac2>
&STDEMBED&
