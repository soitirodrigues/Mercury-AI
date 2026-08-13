class MarketClosedException(Exception):
    """Raised when the market is closed or data is insufficient."""
    pass


class DataValidationError(Exception):
    """Raised when market data fails schema validation (missing columns, NaN, wrong types)."""
    pass


class InvalidSymbolError(Exception):
    """Raised when a symbol fails sanitization (path traversal, invalid chars, empty)."""
    pass


class ProviderError(Exception):
    """Raised when a data provider fails after retries or returns unrecoverable errors."""
    pass


class AuthenticationError(Exception):
    """Raised when authentication fails (missing or invalid credentials)."""
    pass


class InvalidOrderError(Exception):
    """Raised when an order has invalid parameters (quantity, price, etc.)."""
    pass
