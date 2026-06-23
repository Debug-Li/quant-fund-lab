from __future__ import annotations

import pandas as pd


def rsi(data: pd.DataFrame | pd.Series, window: int = 14, column: str = "close") -> pd.Series:
    """Return Wilder-style relative strength index."""
    series = data[column] if isinstance(data, pd.DataFrame) else data
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1 / window, min_periods=window, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / window, min_periods=window, adjust=False).mean()
    rs = avg_gain / avg_loss.replace(0, pd.NA)
    return 100 - (100 / (1 + rs))
