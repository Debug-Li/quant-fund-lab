from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date

import pandas as pd


class BaseDataProvider(ABC):
    source: str

    @abstractmethod
    def fetch_history(
        self,
        symbol: str,
        start: str | date,
        end: str | date | None = None,
        timeframe: str = "1d",
    ) -> pd.DataFrame:
        """Fetch OHLCV market bars normalized to the project schema."""
