from __future__ import annotations

import pandas as pd
import pytest


def build_sample_bars(symbol: str = "TEST") -> pd.DataFrame:
    dates = pd.bdate_range("2024-01-02", periods=80)
    close = pd.Series(range(100, 180), dtype="float64")
    return pd.DataFrame(
        {
            "symbol": symbol,
            "datetime": dates,
            "open": close + 0.1,
            "high": close + 1.0,
            "low": close - 1.0,
            "close": close,
            "volume": 1000,
            "amount": None,
            "adjusted_close": close,
            "source": "test",
            "timeframe": "1d",
        }
    )


@pytest.fixture
def sample_bars():
    return build_sample_bars
