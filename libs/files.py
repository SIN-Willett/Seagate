!gvar edit 71c6b483-2502-4009-ab71-fe4ddf500772
<drac2>
# global variables, allow printing to the final embed
stddesc = []
stdtitle = []
stdfooter = []
stdfields = {}
stdthumb = []
BACKTICK = '`'

def read_file(path, default=None):
  if path[:2] == 'g/':
    return get_gvar(path[2:])
  return get(path, default)

def print(line, ending='\n', file=None):
  if file is None:
    file = stddesc
  file.append(f'{line}{ending}')

def code_block(block, lang=''):
  return f'{BACKTICK * 3}{lang}\n{block}\n{BACKTICK * 3}'

def code_line(line):
  return f'{BACKTICK}{line}{BACKTICK}'

def flush(file):
  return ''.join(file).replace('\"', '\\\"')

def add_field(header, msg):
  stdfields.update({header: msg})

def format_fields():
  lines = [f'-f "{k} | {v}"' for k, v in stdfields.items()]
  return "\n".join(lines)

def show_thumb():
  stdthumb.clear()
  stdthumb.append(f'-thumb <image>')

def hide_thumb():
  stdthumb.clear()

</drac2>