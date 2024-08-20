import requests
import icalendar
import datetime

class CalendarFeed:
    def __init__(self,token):
        self.userToken = token
        pass

    def parseCal(self):
        site = f"https://hcc.instructure.com/feeds/calendars/{userToken}.ics"
        today = datetime.date.today()

        print(site)
        response = requests.get(site)
        content = response.text
        self.calendarFeed = []
        cal = icalendar.Calendar.from_ical(content)
        for component in cal.walk():
            if component.name == "VEVENT":
                assignment = {}
                
                summary = component.get("summary").strip()
                parts = str(summary).replace(']','').split("[")
                
                if(component.get("DESCRIPTION")):
                    description = str(component.get("DESCRIPTION")).strip().replace('\n','').replace('\xa0','')
                else:
                    description = 'No Description'

                if (component.get("X-ALT-DESC")):
                    altDescription = str(component.get("X-ALT-DESC")).strip()
                else:
                    altDescription = 'No alternate description'
                
                url = component.get("URL")
                start = component.decoded("DTSTART")
                start = start.strftime("%m/%d/%Y")

                assignment [str(parts[0]).strip()] = {
                    'course':parts[-1],
                    'description':description,
                    'Due': start,
                    'url':url,
                }

                self.calendarFeed.append(assignment)

userToken = 'user_QjCN6kSXrjOWIfGdYN5kFpHDdpTxooTfnDxVIvIT'
cal = CalendarFeed(userToken)
cal.parseCal()
print(cal.calendarFeed)