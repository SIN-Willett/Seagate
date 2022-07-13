!gvar edit 9d001a76-700f-4df5-a213-311b930b3f0f

using(libs="02488881-7259-4a76-9362-828df7c35a07")
using(
	yaml=libs.find_library("yaml"),
	tm=libs.find_library("time")
)

XP_CC_NAME = 'Experience'
XPLOG_CVAR_NAME = 'xplog'

def load_xplog():
	return yaml.load(XPLOG_CVAR_NAME, {})

def entries_to_lines(entries):
	lines = []
	for k, v in entries.items():
		parts = v.split('|', 1)
		mx = parts[0].strip()
		x = int(mx) if mx.isnumeric() else 0
		m = parts[1].strip() if len(parts) > 1 else mx
		lines.append((k, x, m))
	return lines

def xp_entries_to_str(entries):
	return "\n".join([f"{k[:8]} | {v:7} | {m}" for k, v, m in entries_to_lines(entries)])

def log_xp(xp, message):
	entry = {tm.get_timestamp(): f"{xp} | {message}"}

	log = load_xplog()

	log.update(entry)
	yaml.dump(XPLOG_CVAR_NAME, log, True)

	if not character().cc_exists(XP_CC_NAME):
		character().create_cc(XP_CC_NAME, 0)

	character().mod_cc(XP_CC_NAME, xp)
	return xp_entries_to_str(entry)

def get_xp():
	return character().get_cc(XP_CC_NAME)
