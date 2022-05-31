!gvar edit f5318e22-c75c-460f-96b4-7985b1c2bbd7
from avrae import *
from yaml import *

<drac2>
ETOOLS = get_yaml('eTools', [])
PTOOLS = get_yaml('pTools', [])
PLANGS = get_yaml('languages', [])

def _init_stat(mod, message=None, is_tool=False):
  return {'is_tool': is_tool, 'mod': mod, 'message': message}

def _init_tool(name, mod, message=None):
  prof_level = 2 if name in ETOOLS else 1 if name in PTOOLS else 0
  mod += proficiencyBonus * prof_level
  return _init_stat(mod, message, True)

def _init_lang(name, message=None):
  mod = intelligenceMod
  if name in PLANGS:
    mod += proficiencyBonus
  return _init_stat(mod, message, None)

def _init_arm():
  return _init_stat(character().skills.athletics.value, None, None)

def _init_instr(name):
  return _init_tool(name, charismaMod, f'is playing the {name.lower()}')

_instr_data = get_yaml('g/186f07ad-aeec-435a-a450-c5c47bfc5f39')
INSTRUMENTS = {name: _init_instr(name) for name in _instr_data}

TOOLS = INSTRUMENTS | {name: _init_tool(name, mod, msg) for name, mod, msg in [
  ("Dice Set", charismaMod, "is throwing dice"),
  ("Playing Card Set", charismaMod, "is playing cards"),
  ("Cobbler's Tools", dexterityMod, "is cobbling"),
  ("Disguise Kit", dexterityMod, "has disguised themselves"),
  ("Glassblower's Tools", dexterityMod, "is glassblowing"),
  ("Jeweler's Tools", dexterityMod, "is working on jewelery"),
  ("Potter's Tools", dexterityMod, "is working on pottery"),
  ("Tinker's Tools", dexterityMod, "is tinkering"),
  ("Thieves' Tools", dexterityMod, "is using Thieves' tools"),
  ("Weaver's Tools", dexterityMod, "is weaving"),
  ("Woodcarver's Tools", dexterityMod, "is carving"),
  ("Alchemist's Supplies", intelligenceMod, "is doing alchemy"),
  ("Calligrapher's Supplies", intelligenceMod, "is doing calligraphy"),
  ("Cartographer's Tools", intelligenceMod, "is doing cartography"),
  ("Poisoner's Kit", intelligenceMod, "is working with poisons"),
  ("Carpenter's Tools", strengthMod, "is doing carpentry"),
  ("Leatherworker's Tools", strengthMod, "is doing leatherwork"),
  ("Mason's Tools", strengthMod, "is doing masonary"),
  ("Smith's Tools", strengthMod, "is smithing"),
  ("Brewer's Supplies", wisdomMod, "is brewing"),
  ("Cook's Utensils", wisdomMod, "is cooking"),
  ("Herbalism Kit", wisdomMod, "is working with herbs"),
  ("Painter's Supplies", wisdomMod, "is painting"),
  ("Navigator's Tools", wisdomMod, "is navigating"),
  ("Land Vehicles", strengthMod, None),
  ("Water Vehicles", strengthMod, None),
]}

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
  ("Sleight of Hand", character().skills.sleightOfHand.value, "uses their quick fingers"),
  ("Survival", character().skills.survival.value, "is surviving"),
  ("Stealth", character().skills.stealth.value, "is stealthing"),
  ("Medicine", character().skills.medicine.value, "uses medicinal knowledge"),
  ("Insight", character().skills.insight.value, "is being insightful"),
  ("Religion", character().skills.religion.value, "is being pious"),
  ("Deception", character().skills.deception.value, "is being deceptive"),
  ("Intimidation", character().skills.intimidation.value, "is being intimidating"),
]}

_lang_data = get_yaml('g/3ea94488-2b7f-45e8-a7e3-7b3c8b6a5ec7')
LANGS = { name: _init_lang(name) for name in _lang_data}

_arms_data = get_yaml('g/f9f9b842-9924-48e9-98a3-bc12e739b3df')
ARMS = { name: _init_arm() for name in _arms_data}

STATS = TOOLS | SKILLS | LANGS | ARMS
stats = STATS

def best_stat(stat_choices):
  best = stat_choices[0]
  for choice in stat_choices:
    if STATS[choice].mod > STATS[best].mod:
      best = choice
  return best


character().set_cvar("stats", dump_yaml(stats, 1))
</drac2>