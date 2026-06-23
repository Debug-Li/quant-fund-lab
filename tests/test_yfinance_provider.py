from __future__ import annotations

from quant_fund_lab.market.data.providers.yfinance_provider import _normalize_yahoo_chart_payload


def test_normalize_yahoo_chart_payload() -> None:
    payload = {
        "chart": {
            "result": [
                {
                    "timestamp": [1704162600, 1704249000],
                    "indicators": {
                        "quote": [
                            {
                                "open": [100.0, 101.0],
                                "high": [102.0, 103.0],
                                "low": [99.0, 100.0],
                                "close": [101.0, 102.0],
                                "volume": [1000, 2000],
                            }
                        ],
                        "adjclose": [{"adjclose": [100.5, 101.5]}],
                    },
                }
            ],
            "error": None,
        }
    }
    df = _normalize_yahoo_chart_payload(payload, symbol="SPY", timeframe="1d")

    assert len(df) == 2
    assert df["symbol"].tolist() == ["SPY", "SPY"]
    assert df["source"].tolist() == ["yahoo_chart", "yahoo_chart"]
    assert df["adjusted_close"].tolist() == [100.5, 101.5]
