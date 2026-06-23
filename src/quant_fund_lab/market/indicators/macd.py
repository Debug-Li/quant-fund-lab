from __future__ import annotations

import pandas as pd


def macd(
    data: pd.DataFrame | pd.Series,
    fast: int = 12,
    slow: int = 26,
    signal: int = 9,
    column: str = "close",
) -> pd.DataFrame:
    """Return MACD line, signal line, and histogram."""
    series = data[column] if isinstance(data, pd.DataFrame) else data
    fast_ema = series.ewm(span=fast, adjust=False).mean()
    slow_ema = series.ewm(span=slow, adjust=False).mean()
    macd_line = fast_ema - slow_ema
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line
    return pd.DataFrame({"macd": macd_line, "signal": signal_line, "histogram": histogram})
