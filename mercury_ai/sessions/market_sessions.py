from datetime import datetime


class MarketSessions:

    def get_current_session(self):

        hour = datetime.utcnow().hour

        if 22 <= hour or hour < 7:
            return "Sydney"

        elif 0 <= hour < 9:
            return "Tokyo"

        elif 7 <= hour < 16:
            return "London"

        elif 13 <= hour < 22:
            return "New York"

        return "Closed"

    def is_high_liquidity(self):

        hour = datetime.utcnow().hour

        return 13 <= hour < 16