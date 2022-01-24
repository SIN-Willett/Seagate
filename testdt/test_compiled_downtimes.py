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
    
strargs = str(args)
DT = args[0]

## This is to save a DT
if args[0] == "save":
    return get_gvar("83faff8e-8cdb-4758-9c36-a7882279dfea").replace("&&&", strargs)

## This is to run DTs
if DT == "service":
    return get_gvar("4720b72e-77c9-4f7c-91df-fcb86efe897c").replace("&&&", strargs)

if DT in ["work", "working", "job"]:
    return get_gvar("a74d17ca-00a8-4e43-9ceb-3eb35c5c0c9b").replace("&&&", strargs)

if DT in ["craft", "crafting"]:
    return get_gvar("9f616ca4-939b-44d4-be89-e80f77e89c24").replace("&&&", strargs)

if DT in ["train", "training"]:
    return get_gvar("b378739b-efff-4e99-ae3f-ea00ff58e1d0").replace("&&&", strargs)

if DT in ["study", "studying"]:
    return get_gvar("608a7559-b0f5-4dbf-95d7-b4ce9ffd7cae").replace("&&&", strargs)

return get_gvar("a1adcea5-b563-4e8e-a546-9866919cc415").replace("&&&", strargs)
</drac2>