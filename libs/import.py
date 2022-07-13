"""
Manages library installations
"""


def _build_path(loader):
  return loader('LIBRARY_PATH', '').split(':')


_LIBRARY_PATH = _build_path(get) + \
                _build_path(get_svar) + \
                ['6b06857b-15d4-469e-a4d4-1c7e2915b1d9']


def find_library(lib_name):
  """
  Find a library by name
  If you have an installed LIBRARY_PATH
  look there otherwise look through the
  default LIBRARY_PATH

  :param lib_name: the library's name
  :return: The gvar for that library
  """
  for p in _LIBRARY_PATH:
    if not p:
      continue
    libs = load_yaml(get_gvar(p))
    if lib_name in libs:
      return libs[lib_name]
  return None
