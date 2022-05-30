!gvar edit f6ee7dcf-764d-43e2-97ce-52dadaf266dc
import files

<drac2>
def main(args):
  if not args:
    err(f'usage: {ctx.prefix}drac [cvar | uvar | g/gvar]')
  path = args[0]
  file = read_file(path)
  if not file:
    err(f'could not find file called {path}')
  if path[:2] == 'g/':
    edit_line = f'{ctx.prefix}gvar edit {path[2:]}'
  else:
    edit_line = f'{ctx.prefix}cvar {path}'
  print(code_block(f'{edit_line}\n{file}', 'py'))
main(&&&)
</drac2>
&STDEMBED&