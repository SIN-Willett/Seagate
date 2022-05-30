!gvar edit a3910ffd-c254-4b4e-ad78-fb1c4d37f912
import files
import yaml

<drac2>
def main(args):
  if not args:
    err(f'usage: {ctx.prefix}yaml [cvar | uvar | g/gvar]')
  result = get_yaml(args[0])
  if not result:
    err(f'could not find file called {args[0]}')
  print(code_block(dump_yaml(result), 'yaml'))
main(&&&)
</drac2>
&STDEMBED&
