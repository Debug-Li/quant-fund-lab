from __future__ import annotations

import pandas as pd


def moving_average(data: pd.DataFrame | pd.Series, window: int, column: str = "close") -> pd.Series:
    """Return a simple moving average."""
    series = data[column] if isinstance(data, pd.DataFrame) else data
    return series.rolling(window=window, min_periods=window).mean()
