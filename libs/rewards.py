!gvar edit 71bc1db0-4e38-48c4-9a87-79578eab6901
from avrae import *
from xplog import log_xp

<drac2>
def split_coin(gold):
  if not gold:
    return 0,0,0

  gp = int(gold)
  gold -= gp
  sp = int(gold * 10)
  gold -= sp / 10
  cp = int(gold * 100)
  gold -= cp / 100
  cp += (gold > 0)

  return gp, sp, cp

def reward_cc(cc_name, cc_delta, cc_max, cc_reward):
  self = {
    'name': cc_name,
    'delta': cc_delta,
    'max': cc_max,
    'reward': cc_reward
  }

  def acquire_cc():
    if not character().cc_exists(self.name):
      character().create_cc_nx(self.name, maxVal=self.max, initial_value="0")

    character().mod_cc(self.name, self.delta)
    curr = character().get_cc(self.name)
    max_val = character().get_cc_max(self.name)

    if curr >= max_val:
      character().delete_cc(self.name)
      return self.reward
    return None

  self['acquire'] = acquire_cc

  return self

def reward(msg=None, xp=0, gp=None, special=None, r_cc=None):
  self = {
    'msg':msg, 'xp': xp, 'gp': gp,
    'special': special, 'r_cc': r_cc
  }

  def add_part(this, other):
    if not this:
      return other
    if not other:
      return this
    return this + other

  def add_reward(other):
    if not other:
      pass

    self['msg'] = add_part(self.msg, other.msg)
    self['xp'] = add_part(self.xp, other.xp)
    self['gp'] = add_part(self.gp, other.gp)
    self['special'] = add_part(self.special, other.special)

  self['add'] = add_reward

  def acquire_reward(log_msg):
    if self['r_cc']:
      cc_reward = self['r_cc']['acquire']()
      self['add'](cc_reward)

    log_entry = log_xp(self.xp, log_msg)
    if self.gp:
      g, s, c = split_coin(self.gp)
      character().coinpurse.modify_coins(0, g, 0, s, c)

    return self, log_entry

  self['acquire'] = acquire_reward

  return self
</drac2>