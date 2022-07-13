!gvar edit f5318e22-c75c-460f-96b4-7985b1c2bbd7

using(libs="02488881-7259-4a76-9362-828df7c35a07")
using(yaml=libs.find_library("yaml"))

ETOOLS = yaml.load('eTools', [])
PTOOLS = yaml.load('pTools', [])
PLANGS = yaml.load('languages', [])
PRONOUNS = [p.lower().strip() for p in get('pronouns', 'they/them/their').split('/', 2)]

def _init_stat(mod, message=None, is_tool=False):
  return {'is_tool': is_tool, 'mod': mod, 'message': message}

def _init_tool(name, mod, message=None):
  prof_level = 2 if name in ETOOLS else 1 if name in PTOOLS else 0
  mod += character().stats.prof_bonus * prof_level
  return _init_stat(mod, message, True)

def _init_lang(name, message=None):
  mod = character().stats.get_mod("INT")
  if name in PLANGS:
    mod += character().stats.prof_bonus
  return _init_stat(mod, message, None)

def _init_arm():
  return _init_stat(character().skills.athletics.value, None, None)

def _init_instr(name):
  return _init_tool(name, character().stats.get_mod("CHA"), f'is playing the {name.lower()}')

_instr_data = yaml.load('g/186f07ad-aeec-435a-a450-c5c47bfc5f39')
INSTRUMENTS = {name: _init_instr(name) for name in _instr_data}

_tool_specs = yaml.load("g/041c13c8-9fbc-4fdc-b980-646568f87368")

TOOLS = INSTRUMENTS | {name: _init_tool(name, character().stats.get_mod(mod), msg) for name, mod, msg in _tool_specs}

SKILLS = { name: _init_stat(mod, msg) for name, mod, msg in [
  ("Performance", character().skills.performance.value, "is performing"),
  ("History", character().skills.history.value, "uses historic knowledge"),
  ("Persuasion", character().skills.persuasion.value, "is being persuasive"),
  ("Arcana", character().skills.arcana.value, "uses arcane knowledge"),
  ("Athletics", character().skills.athletics.value, "is being athletic"),
  ("Investigation", character().skills.investigation.value, "is investigating"),
  ("Acrobatics", character().skills.acrobatics.value, "is being acrobatic"),
  ("Animal Handling", character().skills.animalHandling.value, "is handling animals"),
  ("Perception", character().skills.perception.value, "is being perceptive"),
  ("Nature", character().skills.nature.value, "uses natural knowledge"),
  ("Sleight of Hand", character().skills.sleightOfHand.value, f"uses {PRONOUNS[2]} quick fingers"),
  ("Survival", character().skills.survival.value, "is surviving"),
  ("Stealth", character().skills.stealth.value, "is stealthing"),
  ("Medicine", character().skills.medicine.value, "uses medicinal knowledge"),
  ("Insight", character().skills.insight.value, "is being insightful"),
  ("Religion", character().skills.religion.value, "is being pious"),
  ("Deception", character().skills.deception.value, "is being deceptive"),
  ("Intimidation", character().skills.intimidation.value, "is being intimidating"),
]}

_lang_data = yaml.load('g/3ea94488-2b7f-45e8-a7e3-7b3c8b6a5ec7')
LANGS = { name: _init_lang(name) for name in _lang_data}

_arms_data = yaml.load('g/f9f9b842-9924-48e9-98a3-bc12e739b3df')
ARMS = { name: _init_arm() for name in _arms_data}

STATS = TOOLS | SKILLS | LANGS | ARMS
stats = STATS

def best_stat(stat_choices):
  best = stat_choices[0]
  for choice in stat_choices:
    if STATS[choice].mod > STATS[best].mod:
      best = choice
  return best

yaml.dump("stats", stats)
