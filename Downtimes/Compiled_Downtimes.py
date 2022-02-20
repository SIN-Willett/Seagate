tembed
{{get_gvar("2c0daf9b-fc9e-47ee-bd7b-9850ac961d6f")}}
{{create_cc_nx("Experience")}}
{{calendar=load_json(get_gvar("1aec09a0-9e25-4700-9c2d-42d79cb0163b"))}}
{{hourOffset=calendar.get('hourOffset',0)+int(get('timezone',0))}}
{{baseYear=calendar.get("yearOffset",1970)}}
{{Time=time()+(3600*hourOffset)}}
{{totalDayCount=int((Time)//86400)}}
{{yearsPassed=totalDayCount//calendar.length}}
{{numLeapYears=len([x for x in range(baseYear,baseYear+yearsPassed-4) if x//calendar.get('leapCycle',4)==x/calendar.get('leapCycle',4)]) if calendar.get('leapCycle') else 0}}
{{yearStartDay=yearsPassed*calendar.length+numLeapYears}}
{{totalDays=totalDayCount-yearStartDay}}
{{year=int((totalDayCount-numLeapYears-1)//calendar.length)+baseYear}}
{{isLeapYear=year//calendar.get('leapCycle',4)==year/calendar.get('leapCycle',4) if numLeapYears else 0}}
{{calendarDay=totalDays%(calendar.length+isLeapYear) or calendar.length+isLeapYear}}
{{hour=int(Time%86400//3600)}}
{{minute=int(Time%86400%3600//60)}}
{{second=int(Time%86400%3600%60)}}
{{monthLengths=[x.length+(isLeapYear and x.name==calendar.get('leapMonth','February')) for x in calendar.months]}}
{{day,month=calendarDay,1}}
{{[(day:=day-monthLengths[x],month:=month+1) for x in range(len(monthLengths)) if month>x and day>monthLengths[x]]}}
{{timestamp=f'{day:02}.{month:02}.{str(year)[2:]} ({hour:02}:{minute:02}:{second:02})'}}
{{character().set_cvar("Timestamp",timestamp)}} 
<drac2>
## The above timestamp generation is sourced from Derixyleth#0636 xplog alias
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

    if len(args) >= 1:
        args += &ARGS&[1:]
    
strargs = str(args)
DT = args[0]

if DT == "test":
    err("This is the live downtime alias, are you trying to use !testdt ?")

## This is to save a DT
if DT == "save":
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