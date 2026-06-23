from __future__ import annotations

from datetime import date

import pandas as pd
import yfinance as yf

from quant_fund_lab.market.data.providers.base import BaseDataProvider
from quant_fund_lab.utils.exceptions import DataProviderError


class YFinanceProvider(BaseDataProvider):
    source = "yfinance"

    def fetch_history(
        self,
        symbol: str,
        start: str | date,
        end: str | date | None = None,
        timeframe: str = "1d",
    ) -> pd.DataFrame:
        try:
            raw = yf.download(
                symbol,
                start=start,
                end=end,
                interval=timeframe,
                auto_adjust=False,
                progress=False,
            )
        except Exception as exc:  # pragma: no cover - network dependent
            raise DataProviderError(f"yfinance failed for {symbol}: {exc}") from exc

        if raw.empty:
            raise DataProviderError(f"yfinance returned no data for {symbol}")

        if isinstance(raw.columns, pd.MultiIndex):
            raw.columns = raw.columns.get_level_values(0)

        df = raw.reset_index().rename(
            columns={
                "Date": "datetime",
                "Datetime": "datetime",
                "Open": "open",
                "High": "high",
                "Low": "low",
                "Close": "close",
                "Volume": "volume",
                "Adj Close": "adjusted_close",
            }
        )
        df["symbol"] = symbol
        df["source"] = self.source
        df["timeframe"] = timeframe
        if "amount" not in df:
            df["amount"] = None
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
        return df[columns].dropna(subset=["datetime", "open", "high", "low", "close"])
