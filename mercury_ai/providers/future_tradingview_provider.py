class FutureTradingViewProvider:
    def get_data(self, symbol: str, interval: str = "5m", period: str = "5d"):
        raise NotImplementedError("Not implemented")

    def is_available(self) -> bool:
        return False

    def supports_symbol(self, symbol: str) -> bool:
        return False

    def supports_market(self, market: str) -> bool:
        return False

    def supports_timeframe(self, timeframe: str) -> bool:
        return False

    def max_history(self) -> str:
        return "N/A"

    def source_name(self) -> str:
        return "FutureTradingView"
