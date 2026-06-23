class QuantFundError(Exception):
    """Base application exception."""


class DataProviderError(QuantFundError):
    """Raised when a market data provider cannot return usable data."""


class StrategyLoadError(QuantFundError):
    """Raised when a strategy file cannot be loaded."""


class BacktestError(QuantFundError):
    """Raised when backtest execution fails."""
