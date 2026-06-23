from __future__ import annotations

from pathlib import Path

import pandas as pd

from quant_fund_lab.market.data.storage.database import MarketDatabase


class MarketDataRepository:
    def __init__(self, db_path: str | Path | None = None) -> None:
        self.database = MarketDatabase(db_path) if db_path else MarketDatabase()
        self.database.init_schema()

    def save_bars(self, bars: pd.DataFrame) -> int:
        if bars.empty:
            return 0

        df = bars.copy()
        df["datetime"] = pd.to_datetime(df["datetime"])
        required = [
            "symbol",
            "datetime",
            "timeframe",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "amount",
            "adjusted_close",
            "source",
        ]
        for col in required:
            if col not in df:
                df[col] = None
        df = df[required]

        with self.database.connect() as con:
            con.register("incoming_bars", df)
            con.execute(
                """
                DELETE FROM market_bars
                USING incoming_bars
                WHERE market_bars.symbol = incoming_bars.symbol
                  AND market_bars.datetime = incoming_bars.datetime
                  AND market_bars.timeframe = incoming_bars.timeframe
                """
            )
            con.execute(
                """
                INSERT INTO market_bars (
                    symbol, datetime, timeframe, open, high, low, close, volume,
                    amount, adjusted_close, source
                )
                SELECT symbol, datetime, timeframe, open, high, low, close, volume,
                       amount, adjusted_close, source
                FROM incoming_bars
                """
            )
        return len(df)

    def get_bars(
        self,
        symbol: str,
        start: str | None = None,
        end: str | None = None,
        timeframe: str = "1d",
    ) -> pd.DataFrame:
        clauses = ["symbol = ?", "timeframe = ?"]
        params: list[object] = [symbol, timeframe]
        if start:
            clauses.append("datetime >= ?")
            params.append(pd.Timestamp(start).to_pydatetime())
        if end:
            clauses.append("datetime <= ?")
            params.append(pd.Timestamp(end).to_pydatetime())

        query = f"""
            SELECT symbol, datetime, open, high, low, close, volume, amount,
                   adjusted_close, source, timeframe
            FROM market_bars
            WHERE {' AND '.join(clauses)}
            ORDER BY datetime
        """
        with self.database.connect() as con:
            return con.execute(query, params).fetchdf()
