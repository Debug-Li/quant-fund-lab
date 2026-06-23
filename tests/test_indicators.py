from __future__ import annotations

import pandas as pd

from quant_fund_lab.market.indicators import bollinger_bands, macd, moving_average, rsi


def test_indicators_return_expected_shapes() -> None:
    data = pd.DataFrame({"close": [float(i) for i in range(1, 61)]})

    ma = moving_average(data, 5)
    rsi_values = rsi(data, 14)
    macd_values = macd(data)
    bands = bollinger_bands(data, 20)

    assert ma.iloc[4] == 3.0
    assert len(rsi_values) == len(data)
    assert set(macd_values.columns) == {"macd", "signal", "histogram"}
    assert set(bands.columns) == {"middle", "upper", "lower"}
    assert bands["middle"].notna().sum() == 41
