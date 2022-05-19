embed
<drac2>
if get("bags"):
    bags = load_json(get("bags"))
    i = 0
    for bag in bags:
        if bag[0] == "Coin Pouch":
            break
        i = i + 1

    if i == len(bags):
        character().set_cvar('dt_upgrade', 1)
    else"
        ep = 0

        if 'ep' in bags[i][1]:
            ep = int(bags[i][1]['ep'])

        character().coinpurse.set_coins(int(bags[i][1]['pp']), int(bags[i][1]['gp']), ep, int(bags[i][1]['sp']), int(bags[i][1]['cp']))

        bags[i] = ["Pouch", {}]
        character().set_cvar("bags", dump_json(bags))
character().set_cvar('dt_upgrade', 1)

</drac2>

-title "You have converted {{name}}'s coins."
-desc "{{str(character().coinpurse)}}"
-footer "Made by Omie <3"