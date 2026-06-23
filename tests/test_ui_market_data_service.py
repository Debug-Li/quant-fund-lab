from __future__ import annotations

import pandas as pd

from quant_fund_lab.ui.services.market_data_service import add_indicators_service
from quant_fund_lab.ui.services.rotation_service import run_rotation_backtest_service
from quant_fund_lab.ui.services.signal_service import generate_latest_signal_service


def test_add_indicators_service() -> None:
    bars = pd.DataFrame(
        {
            "datetime": pd.bdate_range("2024-01-01", periods=80),
            "open": range(80),
            "high": range(1, 81),
            "low": range(80),
            "close": range(1, 81),
            "volume": 1000,
        }
    )
    result = add_indicators_service(bars, ["MA", "RSI", "MACD", "Bollinger"])
    assert result.success is True
    assert {"ma_5", "rsi", "macd", "bb_upper"}.issubset(result.dataframe.columns)


def test_signal_service_missing_matrix_returns_friendly_error(monkeypatch) -> None:
    import quant_fund_lab.ui.services.signal_service as signal_service

    def missing():
        raise FileNotFoundError("missing")

    monkeypatch.setattr(signal_service, "load_price_matrix", missing)
    result = generate_latest_signal_service()
    assert result.success is False
    assert "数据中心" in result.message


def test_rotation_service_missing_matrix_returns_friendly_error(monkeypatch) -> None:
    import quant_fund_lab.ui.services.rotation_service as rotation_service

    def missing():
        raise FileNotFoundError("missing")

    monkeypatch.setattr(rotation_service, "load_price_matrix", missing)
    result = run_rotation_backtest_service(60, 3, 20)
    assert result.success is False
    assert "数据中心" in result.message
