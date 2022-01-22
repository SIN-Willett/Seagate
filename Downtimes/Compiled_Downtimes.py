#1d644726-7dde-4e11-9ebf-aa15d1c155ff
tembed
{{get_gvar("2c0daf9b-fc9e-47ee-bd7b-9850ac961d6f")}}
<drac2>
args = &ARGS&

## This is to sub in a saved DT
if args[0].isnumeric():
    index = args[0]
    DTsaved = get("DTsaved")
    
    if not DTsaved:
        err("Use !dt save or !downtime save " + index + " the downtime deatils you want to save to this number.")
    
    possible = load_json(DTsaved)
    
    if index not in possible:
        err("There is no downtime saved to " + index)
    
    args = possible[index]
    
strargs = str(args)
DT = args[0]

## This is to save a DT
if args[0] == "save":
    return get_gvar("83faff8e-8cdb-4758-9c36-a7882279dfea").replace("&&&", strargs)

## This is to run DTs
if DT == "service":
    return get_gvar("e55f5a53-b70a-484d-a386-6acc350d2c0d").replace("&&&", strargs)

if DT in ["work", "working", "job"]:
    return get_gvar("1231c3de-651d-4d19-abfe-185c09b785c7").replace("&&&", strargs)

if DT in ["craft", "crafting"]:
    return get_gvar("4bd5ceb6-e82f-4196-be25-988c6c4e2a3d").replace("&&&", strargs)

if DT in ["train", "training"]:
    return get_gvar("585d1453-7303-44a5-b736-f707c2702b5e").replace("&&&", strargs)

if DT in ["study", "studying"]:
    return get_gvar("97d2dddb-2116-41e3-a312-44351619d3eb").replace("&&&", strargs)

return get_gvar("da0f7936-97bd-472c-b3fd-f72622df20e4").replace("&&&", strargs)
</drac2>