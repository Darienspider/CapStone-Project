import calendarFeed


userToken = 'user_QjCN6kSXrjOWIfGdYN5kFpHDdpTxooTfnDxVIvIT'
cal = calendarFeed.CalendarFeed(userToken)
extraction = cal.parseCal()
print(extraction)