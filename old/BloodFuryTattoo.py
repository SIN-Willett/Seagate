<drac2>
damage = 'None'
desc = "When you hit a creature with a weapon attack, you can expend a charge to deal an extra 4d6 necrotic damage to the target, and you regain a number of hit points equal to the necrotic damage dealt."
cc = "Blood Fury Tattoo"
ability = "Bloodthirsty Strike"
noCC = "You do not have this ability."
dawn = "You can't use this item again until the next dawn."
char = character()
succ = "and tries to use a"
miss =  get('miss', 0) + (not get_cc(cc) > 0)

if char.cc_exists(cc) and char.get_cc(cc) and miss:
    succ = "using a"
    damage = "-d 4d6[necrotic]"
    D = desc
    char.mod_cc(cc, -1)
elif char.cc_exists(cc):
    D = dawn
else:
    D = noCC
T = f"{succ} {ability}"
F = f"{cc}|{char.cc_str(cc) if char.cc_exists(cc) else '*None*'}"
</drac2>
-title "[name] [verb] [aname] {{T}}"
-f "Bloodthirsty Strikes|{{D}}"
-f "{{F}}"
{{damage}}


!snippet ammo {{c = 'Ammo'}}
{{C, ammoF = 'Used ' + c, get('ammoF', 0) + 1}}
{{create_cc_nx(C, 0)}}
{{(create_cc_nx(c, 0), set_cc(c, 20)) if not cc_exists(c) else ''}}
{{v = get_cc(c) > 0}}
{{miss = get('miss', 0) + (not v)}}
{{(mod_cc(c, -1), mod_cc(C, 1)) if v else f'miss{miss}'}}
{{f'-phrase "{"Using a piece of ammunition" if ammoF == 1 else "...and another one"} ({get_cc(c)} remaining)"'}}
{{'' if ammoF > 1 else '-f "Ammunition|You can use a weapon that has the ammunition property to make a ranged attack only if you have ammunition to fire from the weapon. (PHB 146)"'}}