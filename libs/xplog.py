!gvar edit 9d001a76-700f-4df5-a213-311b930b3f0f
from avrae import *
from yaml import *
from time import *

<drac2>
XP_CC_NAME = 'Experience'
XPLOG_CVAR_NAME = 'xplog'


def entries_to_lines(entries):
	lines = []
	for k, v in entries.items():
		parts = v.split('|', 1)
		x = int(parts[0].strip())
		m = parts[1].strip()
		lines.append((k, x, m))
	return lines

def xp_entries_to_str(entries):
	return "\n".join([f"{k[:8]} | {v:7} | {m}" for k, v, m in entries_to_lines(entries)])

def log_xp(xp, message):
	entry = {get_timestamp(): f"{xp} | {message}"}

	log = get_yaml(XPLOG_CVAR_NAME, {})

	log.update(entry)
	set_json(XPLOG_CVAR_NAME, log)

	if not character().cc_exists(XP_CC_NAME):
		character().create_cc(XP_CC_NAME, 0)

	character().mod_cc(XP_CC_NAME, xp)

	out = xp_entries_to_str(entry)
	add_field("XP Log entry added:", f"{code_block(out)}")
	return entry

def get_xp():
	return character().get_cc(XP_CC_NAME)
</drac2>