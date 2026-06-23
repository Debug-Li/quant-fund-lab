from __future__ import annotations

from datetime import date

import pandas as pd

from quant_fund_lab.data.akshare_loader import fetch_etf_daily
from quant_fund_lab.market.data.providers.base import BaseDataProvider
from quant_fund_lab.utils.exceptions import DataProviderError


class AKShareProvider(BaseDataProvider):
    source = "akshare"

    def fetch_history(
        self,
        symbol: str,
        start: str | date,
        end: str | date | None = None,
        timeframe: str = "1d",
    ) -> pd.DataFrame:
        if timeframe not in {"1d", "daily"}:
            raise DataProviderError("AKShare MVP provider currently supports daily ETF data only.")

        start_date = pd.Timestamp(start).strftime("%Y%m%d")
        end_date = pd.Timestamp(end).strftime("%Y%m%d") if end else None
        try:
            raw = fetch_etf_daily(symbol=symbol, name=symbol, start_date=start_date, end_date=end_date)
        except Exception as exc:  # pragma: no cover - network dependent
            raise DataProviderError(f"AKShare failed for {symbol}: {exc}") from exc

        df = raw.rename(columns={"date": "datetime"}).copy()
        df["source"] = self.source
        df["timeframe"] = "1d"
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
