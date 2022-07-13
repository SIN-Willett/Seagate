!gvar edit bca66407-b5be-4daf-95a2-76e1dd412086
using(libs="02488881-7259-4a76-9362-828df7c35a07")
using(yaml=libs.find_library("yaml"))

calendar = yaml.load('g/1aec09a0-9e25-4700-9c2d-42d79cb0163b')

def format_date(tm):
	return f'{tm.day:02}.{tm.month:02}.{str(tm.year)[2:]}'

def format_time(tm):
	return f'{format_date(tm)} ({tm.hour:02}:{tm.minute:02}:{tm.second:02})'

def parse_time(t_since_epoch):
	hourOffset = calendar.get('hourOffset', 0) + int(get_yaml('timezone', 0))
	baseYear = calendar.get('yearOffset', 1970)
	leapCycle = calendar.get('leapCycle', 4)

	Time = t_since_epoch + (3600 * hourOffset)
	totalDayCount = int(Time // 86400)
	yearsPassed = totalDayCount // calendar.length
	numLeapYears = len([x for x in range(baseYear, baseYear + yearsPassed - 4) if not (x % leapCycle)]) if leapCycle else 0
	yearStartDay = yearsPassed * calendar.length + numLeapYears
	totalDays = totalDayCount - yearStartDay
	year = int((totalDayCount - numLeapYears - 1) // calendar.length) + baseYear
	isLeapYear = not (year % leapCycle) if numLeapYears else 0
	calendarDay = totalDays % (calendar.length + isLeapYear) or calendar.length + isLeapYear
	hour = int(Time % 86400 // 3600)
	minute = int(Time % 86400 % 3600 // 60)
	second = int(Time % 86400 % 3600 % 60)
	monthLengths = [x.length + (isLeapYear and x.name == calendar.get('leapMonth','February')) for x in calendar.months]
	day, month = calendarDay, 1
	[(day := day - monthLengths[x], month := month + 1) for x in range(len(monthLengths)) if month > x and day > monthLengths[x]]
	return {'day': day, 'month': month, 'year': year, 'hour': hour, 'minute': minute, 'second': second}

def get_timestamp():
	return format_time(parse_time(time()))

def get_datestamp():
	return format_date(parse_time(time()))