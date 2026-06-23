from __future__ import annotations

from datetime import date

import akshare as ak
import pandas as pd

from quant_fund_lab.market.data.providers.base import BaseDataProvider
from quant_fund_lab.utils.exceptions import DataProviderError


class AKShareProvider(BaseDataProvider):
    source = "akshare"

    def __init__(self, asset_type: str = "etf", adjust: str = "qfq") -> None:
        self.asset_type = asset_type
        self.adjust = adjust

    def fetch_history(
        self,
        symbol: str,
        start: str | date,
        end: str | date | None = None,
        timeframe: str = "1d",
    ) -> pd.DataFrame:
        period = _to_akshare_period(timeframe)
        start_date = pd.Timestamp(start).strftime("%Y%m%d")
        end_date = pd.Timestamp(end).strftime("%Y%m%d") if end else None
        try:
            raw = self._fetch_raw(symbol=symbol, start_date=start_date, end_date=end_date, period=period)
        except Exception as exc:  # pragma: no cover - network dependent
            raise DataProviderError(f"AKShare {self.asset_type} failed for {symbol}: {exc}") from exc

        df = _normalize_akshare_hist(raw, symbol=symbol)
        df["source"] = f"{self.source}_{self.asset_type}"
        df["timeframe"] = timeframe
        if "adjusted_close" not in df:
            df["adjusted_close"] = df["close"]
        columns = [
            "symbol",
            "datetime",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "amount",
            "adjusted_close",
            "source",
            "timeframe",
        ]
        return df[columns]

    def _fetch_raw(self, symbol: str, start_date: str, end_date: str | None, period: str) -> pd.DataFrame:
        if self.asset_type == "stock":
            return ak.stock_zh_a_hist(
                symbol=symbol,
                period=period,
                start_date=start_date,
                end_date=end_date or "20500101",
                adjust=self.adjust,
            )
        if self.asset_type == "index":
            return ak.index_zh_a_hist(
                symbol=symbol,
                period=period,
                start_date=start_date,
                end_date=end_date or "22220101",
            )
        if self.asset_type == "etf":
            return ak.fund_etf_hist_em(
                symbol=symbol,
                period=period,
                start_date=start_date,
                end_date=end_date or "20500101",
                adjust=self.adjust,
            )
        raise DataProviderError(f"Unsupported AKShare asset_type: {self.asset_type}")


def _to_akshare_period(timeframe: str) -> str:
    mapping = {
        "1d": "daily",
        "daily": "daily",
        "1wk": "weekly",
        "weekly": "weekly",
        "1mo": "monthly",
        "monthly": "monthly",
    }
    try:
        return mapping[timeframe]
    except KeyError as exc:
        raise DataProviderError(f"AKShare only supports 1d/1wk/1mo, got: {timeframe}") from exc


def _normalize_akshare_hist(raw: pd.DataFrame, symbol: str) -> pd.DataFrame:
    column_map = {
        "日期": "datetime",
        "时间": "datetime",
        "开盘": "open",
        "收盘": "close",
        "最高": "high",
        "最低": "low",
        "成交量": "volume",
        "成交额": "amount",
        "振幅": "amplitude",
        "涨跌幅": "pct_change",
        "涨跌额": "change",
        "换手率": "turnover",
    }
    df = raw.rename(columns=column_map).copy()
    if "datetime" not in df.columns or "close" not in df.columns:
        raise DataProviderError(f"AKShare returned unexpected columns: {list(raw.columns)}")

    df["datetime"] = pd.to_datetime(df["datetime"])
    for col in [c for c in df.columns if c not in {"datetime"}]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["symbol"] = symbol
    if "amount" not in df.columns:
        df["amount"] = None
    return df.sort_values("datetime").reset_index(drop=True)
