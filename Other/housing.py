embed <drac2>
cc = "Inspiration"
exhaust = "Exhaustion"
myroll = vroll(f"1d4").total
character().create_cc_nx(exhaust,0,6,"long","bubble",None, -1)
points = character().get_cc(exhaust)
result = load_json(get_gvar("018da0e0-0db5-46e1-9567-f895374f5fdb"))[myroll -1]
character().create_cc_nx(cc,0,1)
if myroll == 2:
    character().set_cc(cc,1)
elif myroll == 3:
    character().set_cc(exhaust,0)
</drac2>
-title "{{name}} rolls for housing benefits!"
-desc "**Housing Benefits:** {{myroll}}
{{name}}{{result}}"
<drac2>
if myroll == 2:
    return f'-f "{cc} (+1)|{"◉"*character().get_cc(cc)}{"〇"*(character().get_cc_max(cc)-character().get_cc(cc))}"'
elif myroll == 3:
    return f'-f "{exhaust} (-{points})|{"◉"*character().get_cc(exhaust)}{"〇"*(character().get_cc_max(exhaust)-character().get_cc(exhaust))}"'
</drac2>
-footer "Made by Omen"
-color <color> -thumb <image>