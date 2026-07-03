from datetime import datetime


class EconomicCalendar:

    def get_events(self):

        today = datetime.now().strftime("%Y-%m-%d")

        events = [
            {
                "country": "USD",
                "event": "Non-Farm Payroll",
                "impact": "High",
                "time": "09:30",
                "forecast": "185K",
                "previous": "177K",
                "actual": None,
                "date": today,
            },
            {
                "country": "USD",
                "event": "FOMC Meeting",
                "impact": "High",
                "time": "15:00",
                "forecast": None,
                "previous": None,
                "actual": None,
                "date": today,
            },
        ]

        return events