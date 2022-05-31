from avrae.character import AliasCharacter
from avrae.combat import SimpleCombat
from avrae.context import AliasContext
from avrae.functions import \
  SimpleRollResult

ctx = AliasContext(None)

def combat(self) -> SimpleCombat:
  """
Returns the combat active in the channel if one is. Otherwise, returns ``None``.
:rtype: :class:`~aliasing.api.combat.SimpleCombat`
"""
  if "combat" not in self._cache:
    self._cache["combat"] = combat_api.SimpleCombat.from_ctx(self.ctx, interpreter=self)
  self.combat_changed = True
  return self._cache["combat"]

def character() -> AliasCharacter:
  """
Returns the active character if one is. Otherwise, raises a :exc:`FunctionRequiresCharacter` error.
:rtype: :class:`~aliasing.api.character.AliasCharacter`
"""
  if "character" not in self._cache:
    raise FunctionRequiresCharacter()
  self.character_changed = True
  return self._cache["character"]

def uvar_exists(name):
  """
Returns whether a uvar exists.
:rtype: bool
"""
  name = str(name)
  return self.exists(name) and name in self._cache["uvars"]

def get_gvar(address):
  """
Retrieves and returns the value of a gvar (global variable).
:param str address: The gvar address.
:return: The value of the gvar.
:rtype: str
"""
  address = str(address)
  if address not in self._cache["gvars"]:
    result = self.ctx.bot.mdb.gvars.delegate.find_one({"key": address})
    if result is None:
      return None
    self._cache["gvars"][address] = result["value"]
  return self._cache["gvars"][address]

def get_svar(name, default=None):
  """
Retrieves and returns the value of a svar (server variable).
:param str name: The name of the svar.
:param default: What to return if the name is not set.
:return: The value of the svar, or the default value if it does not exist.
:rtype: str or None
"""
  name = str(name)
  if self.ctx.guild is None:
    return default
  if name not in self._cache["svars"]:
    result = self.ctx.bot.mdb.svars.delegate.find_one({"owner": self.ctx.guild.id, "name": name})
    if result is None:
      return default
    self._cache["svars"][name] = result["value"]
  return self._cache["svars"][name]

def set_uvar(name: str, value: str):
  """
Sets a user variable.
:param str name: The name of the variable to set.
:param str value: The value to set it to.
"""
  name = str(name)
  value = str(value)
  if not name.isidentifier():
    raise InvalidArgument("Uvar contains invalid character.")
  self._cache["uvars"][name] = value
  self._names[name] = value
  self.uvars_changed.add(name)

def set_uvar_nx(name, value: str):
  """
Sets a user variable if there is not already an existing name.
:param str name: The name of the variable to set.
:param str value: The value to set it to.
"""
  name = str(name)
  if not name in self.names:
    self.set_uvar(name, value)

def delete_uvar(name):
  """
Deletes a user variable. Does nothing if the variable does not exist.
:param str name: The name of the variable to delete.
"""
  name = str(name)
  if name in self._cache["uvars"]:
    del self._cache["uvars"][name]
    self.uvars_changed.add(name)

def get(name, default=None):
  """
  Gets the value of a name, or returns *default* if the name is not set.
  Retrieves names in the order of local > cvar > uvar. Does not interact with svars.
  :param str name: The name to retrieve.
  :param default: What to return if the name is not set.
  """
  name = str(name)
  if name in self.names:
    return self.names[name]
  return default

def load_yaml(yamlstr):
  """
  Loads an object from a YAML string. See `yaml.safe_load <https://pyyaml.org/wiki/PyYAMLDocumentation>`_.
  """
  return yaml.load(str(yamlstr), self._yaml_loader)

def dump_yaml(obj, indent=2):
  """
  Serializes an object to a YAML string. See `yaml.safe_dump <https://pyyaml.org/wiki/PyYAMLDocumentation>`_.
  """
  return yaml.dump(
    obj, Dumper=self._yaml_dumper, default_flow_style=False, line_break=True, indent=indent, sort_keys=False
  )

def load_json(jsonstr):
  """
  Loads an object from a JSON string. See :func:`json.loads`.
  """
  return json.loads(str(jsonstr), cls=self._json_decoder())

def dump_json(obj):
  """
  Serializes an object to a JSON string. See :func:`json.dumps`.
  """
  return json.dumps(obj, default=self._dump_json_default)

def vroll(dice, multiply=1, add=0) -> SimpleRollResult:
  """
  Rolls dice and returns a detailed roll result.

  :param str dice: The dice to roll.
  :param int multiply: How many times to multiply each set of dice by.
  :param int add: How many dice to add to each set of dice.
  :return: The result of the roll.
  :rtype: :class:`~aliasing.api.functions.SimpleRollResult`
  """
  return _vroll(str(dice), int(multiply), int(add))