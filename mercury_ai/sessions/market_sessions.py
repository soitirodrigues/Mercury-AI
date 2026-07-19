from datetime import datetime
from mercury_ai.config import sessions


class MarketSessions:

    def get_current_session(self):

        hour = datetime.utcnow().hour

        if 22 <= hour or hour < 7:
            return sessions.SYDNEY

        elif 0 <= hour < 9:
            return sessions.TOKYO

        elif 7 <= hour < 16:
            return sessions.LONDON

        elif 13 <= hour < 22:
            return sessions.NEW_YORK

        return sessions.CLOSED

    def is_high_liquidity(self):

        hour = datetime.utcnow().hour

        return 13 <= hour < 16