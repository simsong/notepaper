Upgrades for Notepaper2:
* When run on a Mac, read the task list from the Remidners app
Options for interace:
* iCal's Apple events: https://stackoverflow.com/questions/1667693/get-set-calendar-events-on-ical-programmatically
>>> from appscript import *
>>> calendar=app('iCal').calendars['Home']
>>> from datetime import datetime
>>> start_time = datetime(2019,12,1)
>>> end_time = datetime(2019,12,31)
>>> for event in calendar.events[(its.start_date >= start_time).AND(its.start_date <= end_time)]():
...     print(event)
...     print(event.properties())


notification:
osascript -e 'display notification "not" with title "tit"'
