!gvar edit c78f2204-e980-44f4-bd62-59d8ec55438a
using(libs="02488881-7259-4a76-9362-828df7c35a07")
using(io=libs.find_library("io"))

def load(path, default=None):
  yaml = io.read_file(path)
  if not yaml:
    return default
  return load_yaml(yaml)

def dump(key, value, to_json=False):
  dumper = dump_json if to_json else dump_yaml
  character().set_cvar(key, dumper(value))

def append(key, value):
  collection = load(key, [])
  collection.append(value)
  dump(key, collection)
