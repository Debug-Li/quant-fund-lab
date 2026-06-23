from __future__ import annotations

from datetime import date
from pathlib import Path

import pandas as pd

from quant_fund_lab.market.data.providers.base import BaseDataProvider
from quant_fund_lab.utils.exceptions import DataProviderError


class CSVProvider(BaseDataProvider):
    source = "csv"

    def __init__(self, csv_path: str | Path) -> None:
        self.csv_path = Path(csv_path)

    def fetch_history(
        self,
        symbol: str,
        start: str | date,
        end: str | date | None = None,
        timeframe: str = "1d",
    ) -> pd.DataFrame:
        if not self.csv_path.exists():
            raise DataProviderError(f"CSV file not found: {self.csv_path}")

        df = pd.read_csv(self.csv_path)
        df.columns = [col.lower() for col in df.columns]
        if "date" in df.columns and "datetime" not in df.columns:
            df = df.rename(columns={"date": "datetime"})
        if "symbol" not in df.columns:
            df["symbol"] = symbol

        df["datetime"] = pd.to_datetime(df["datetime"])
        mask = df["symbol"].astype(str) == str(symbol)
        mask &= df["datetime"] >= pd.Timestamp(start)
        if end is not None:
            mask &= df["datetime"] <= pd.Timestamp(end)
        df = df.loc[mask].copy()

        if df.empty:
            raise DataProviderError(f"CSV returned no data for {symbol}")

        for col in ["amount", "adjusted_close"]:
            if col not in df:
                df[col] = None
        df["source"] = self.source
        df["timeframe"] = timeframe
        return df[
            [
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
        ].sort_values("datetime")
