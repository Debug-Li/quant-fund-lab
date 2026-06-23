from __future__ import annotations

from pathlib import Path

import pandas as pd

from quant_fund_lab.market.data.providers.akshare_provider import AKShareProvider
from quant_fund_lab.market.data.providers.base import BaseDataProvider
from quant_fund_lab.market.data.providers.csv_provider import CSVProvider
from quant_fund_lab.market.data.providers.yfinance_provider import YFinanceProvider
from quant_fund_lab.market.data.storage.market_data_repository import MarketDataRepository
from quant_fund_lab.utils.exceptions import DataProviderError


def provider_for_market(market: str, csv_path: str | Path | None = None) -> BaseDataProvider:
    normalized = market.lower()
    if normalized in {"us", "美股", "etf", "crypto", "加密货币", "index", "指数"}:
        return YFinanceProvider()
    if normalized in {"a", "a股", "cn", "china", "akshare", "a股股票", "akshare_stock", "cn_stock"}:
        return AKShareProvider(asset_type="stock")
    if normalized in {"a股etf", "akshare_etf", "cn_etf"}:
        return AKShareProvider(asset_type="etf")
    if normalized in {"a股指数", "akshare_index", "cn_index"}:
        return AKShareProvider(asset_type="index")
    if normalized == "csv":
        if csv_path is None:
            raise DataProviderError("csv_path is required for CSV provider.")
        return CSVProvider(csv_path)
    raise DataProviderError(f"Unsupported market: {market}")


def fetch_save_and_query(
    symbol: str,
    market: str,
    start: str,
    end: str | None = None,
    timeframe: str = "1d",
    csv_path: str | Path | None = None,
    repository: MarketDataRepository | None = None,
) -> pd.DataFrame:
    provider = provider_for_market(market, csv_path=csv_path)
    repo = repository or MarketDataRepository()
    bars = provider.fetch_history(symbol=symbol, start=start, end=end, timeframe=timeframe)
    repo.save_bars(bars)
    return repo.get_bars(symbol=symbol, start=start, end=end, timeframe=timeframe)
