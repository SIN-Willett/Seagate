!gvar edit 9d001a76-700f-4df5-a213-311b930b3f0f
from avrae import *
from yaml import *
from time import *

<drac2>
XP_CC_NAME = 'Experience'
XPLOG_CVAR_NAME = 'xplog'

def log_xp(xp, message):
	entry = {get_timestamp(): f'{xp} | {message}'}

	log = get_yaml(XPLOG_CVAR_NAME, {})

	log.update(entry)
	set_json(XPLOG_CVAR_NAME, log)

	if not character().cc_exists(XP_CC_NAME):
		character().create_cc(XP_CC_NAME, 0)

	character().mod_cc(XP_CC_NAME, xp)

	return entry
</drac2>