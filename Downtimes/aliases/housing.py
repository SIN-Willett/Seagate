embed <drac2>
cc = "Inspiration"
exhaust = "Exhaustion"
myroll = vroll(f"1d4").total
create_cc_nx(exhaust,0,6,"long","bubble",None, -1)
points = get_cc(exhaust)
result = load_json(get_gvar("018da0e0-0db5-46e1-9567-f895374f5fdb"))[myroll -1]
create_cc_nx(cc,0,1)
if myroll == 2:
    set_cc(cc,1)
elif myroll == 3:
    set_cc(exhaust,0)
</drac2>
-title "{{name}} rolls for housing benefits!"
-desc "**Housing Benefits:** {{myroll}}
{{name}}{{result}}"
<drac2>
if myroll == 2:
    return f'-f "{cc} (+1)|{"◉"*get_cc(cc)}{"〇"*(get_cc_max(cc)-get_cc(cc))}"'
elif myroll == 3:
    return f'-f "{exhaust} (-{points})|{"◉"*get_cc(exhaust)}{"〇"*(get_cc_max(exhaust)-get_cc(exhaust))}"'
</drac2>
-footer "Made by Omen"
-color <color> -thumb <image>