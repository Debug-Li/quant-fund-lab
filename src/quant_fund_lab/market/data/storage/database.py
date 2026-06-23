from __future__ import annotations

from pathlib import Path

import duckdb

from quant_fund_lab.config.settings import settings


class MarketDatabase:
    def __init__(self, path: str | Path = settings.database_path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def connect(self) -> duckdb.DuckDBPyConnection:
        return duckdb.connect(str(self.path))

    def init_schema(self) -> None:
        with self.connect() as con:
            con.execute(
                """
                CREATE TABLE IF NOT EXISTS market_bars (
                    symbol VARCHAR NOT NULL,
                    datetime TIMESTAMP NOT NULL,
                    timeframe VARCHAR NOT NULL,
                    open DOUBLE NOT NULL,
                    high DOUBLE NOT NULL,
                    low DOUBLE NOT NULL,
                    close DOUBLE NOT NULL,
                    volume DOUBLE,
                    amount DOUBLE,
                    adjusted_close DOUBLE,
                    source VARCHAR NOT NULL,
                    updated_at TIMESTAMP DEFAULT current_timestamp
                )
                """
            )
