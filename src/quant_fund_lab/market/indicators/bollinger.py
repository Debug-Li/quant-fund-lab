from __future__ import annotations

import pandas as pd


def bollinger_bands(
    data: pd.DataFrame | pd.Series,
    window: int = 20,
    num_std: float = 2.0,
    column: str = "close",
) -> pd.DataFrame:
    """Return middle, upper, and lower Bollinger Bands."""
    series = data[column] if isinstance(data, pd.DataFrame) else data
    middle = series.rolling(window=window, min_periods=window).mean()
    std = series.rolling(window=window, min_periods=window).std()
    upper = middle + num_std * std
    lower = middle - num_std * std
    return pd.DataFrame({"middle": middle, "upper": upper, "lower": lower})
