import requests
import icalendar
import datetime

class CalendarFeed:
    def __init__(self,token):
        self.userToken = token
        pass

    def parseCal(self):
        site = f"https://hcc.instructure.com/feeds/calendars/{self.userToken}.ics"
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

                assignment= {
                    'title':str(parts[0]).strip(),
                    'course':parts[-1],
                    'description':description,
                    'due_date': start,
                    'url':url,
                    'status':'Not Submitted'
                }

                self.calendarFeed.append(assignment)
        return self.calendarFeed


userToken = 'user_QjCN6kSXrjOWIfGdYN5kFpHDdpTxooTfnDxVIvIT'
test = CalendarFeed(userToken)
test.parseCal()
for i in test.calendarFeed:
    print(i['title'])