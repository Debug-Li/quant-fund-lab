from __future__ import annotations

import pandas as pd

from quant_fund_lab.market.data.providers.akshare_provider import AKShareProvider
from quant_fund_lab.market.data.providers.csv_provider import CSVProvider
from quant_fund_lab.market.data.providers.yfinance_provider import YFinanceProvider
from quant_fund_lab.market.services.data_service import provider_for_market
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


def test_provider_for_market_routes_new_channels() -> None:
    assert isinstance(provider_for_market("us"), YFinanceProvider)
    assert isinstance(provider_for_market("a股股票"), AKShareProvider)
    assert provider_for_market("a股股票").asset_type == "stock"
    assert provider_for_market("a股ETF").asset_type == "etf"
    assert provider_for_market("a股指数").asset_type == "index"
    assert isinstance(provider_for_market("csv", csv_path="sample.csv"), CSVProvider)


def test_index_fetch_error_has_actionable_hint(monkeypatch) -> None:
    import quant_fund_lab.ui.services.market_data_service as market_data_service

    def bad_fetch(*args, **kwargs):
        raise RuntimeError("AKShare index failed")

    monkeypatch.setattr(market_data_service, "fetch_save_and_query", bad_fetch)
    result = market_data_service.fetch_market_bars_service("000300", "a股指数", "2024-01-01", "2024-06-30", "1d")
    assert result.success is False
    assert "对应 ETF" in result.message
