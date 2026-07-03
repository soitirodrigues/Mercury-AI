from mercury_ai.calendar.economic_calendar import EconomicCalendar

calendar = EconomicCalendar()

events = calendar.get_events()

for event in events:
    print(event)