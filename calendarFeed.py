import requests
import icalendar
import datetime
import json 
import os
import sys

class CalendarFeed:
    def __init__(self,token):
        self.userToken = token
        if getattr(sys, 'frozen', False):
            # If the application is running as an executable
            application_path = os.path.dirname(sys.executable)
        else:
            # If the application is running as a script
            application_path = os.path.dirname(os.path.abspath(__file__))
        
        self.calFeedStatus = os.path.join(application_path, 'calFeed.json')
        print(self.calFeedStatus)
        pass

    def parseCal(self):
        site = f"https://hcc.instructure.com/feeds/calendars/{self.userToken}.ics"
        today = datetime.date.today()

        try:
            self.currentData = json.load(open(self.calFeedStatus))
        except:
            self.currentData = None

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

                # # if file exists - query for current data
                if self.currentData:
                    for eachAssignment in self.currentData:
                #     # if the assignment exists in file - update the status
                    
                        for eachAssignment in self.currentData:
                            if eachAssignment['title'] == str(parts[0]).strip():
                                assignment= {
                                    'title':str(parts[0]).strip(),
                                    'course':parts[-1],
                                    'description':description,
                                    'due_date': start,
                                    'url':url,
                                    'status':eachAssignment['status']
                        }
                                  # Break out of the loop once a match is found

                else:
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
    
    def updateFile(self):
        with open('calFeed.json','w') as f:
            json.dump(self.calendarFeed, f, indent=4)
            f.close()

