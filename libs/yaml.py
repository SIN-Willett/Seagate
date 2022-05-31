!gvar edit c78f2204-e980-44f4-bd62-59d8ec55438a
from avrae import *
from files import *

<drac2>
def get_yaml(path, default=None):
  yaml = read_file(path)
  if not yaml:
    return default
  return load_yaml(yaml)

def set_yaml(key, value):
  yaml = dump_yaml(value)
  character().set_cvar(key, yaml)

def set_json(key, value):
  json = dump_json(value)
  character().set_cvar(key, json)

def append_yaml(key, value):
  collection = get_yaml(key, [])
  collection.append(value)
  set_yaml(key, collection)

</drac2>