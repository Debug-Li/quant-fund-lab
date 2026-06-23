from __future__ import annotations

import pandas as pd

from quant_fund_lab.market.data.storage.market_data_repository import MarketDataRepository


def test_repository_saves_queries_and_replaces_duplicates(tmp_path, sample_bars) -> None:
    db_path = tmp_path / "market_data.duckdb"
    repo = MarketDataRepository(db_path)
    bars = sample_bars("AAA").head(5)

    assert repo.save_bars(bars) == 5
    assert repo.save_bars(bars) == 5

    loaded = repo.get_bars("AAA")
    assert len(loaded) == 5
    assert loaded["symbol"].unique().tolist() == ["AAA"]


def test_repository_date_range(tmp_path, sample_bars) -> None:
    repo = MarketDataRepository(tmp_path / "market_data.duckdb")
    bars = sample_bars("AAA")
    repo.save_bars(bars)

    loaded = repo.get_bars("AAA", start="2024-01-10", end="2024-01-20")
    assert not loaded.empty
    assert loaded["datetime"].min() >= pd.Timestamp("2024-01-10")
    assert loaded["datetime"].max() <= pd.Timestamp("2024-01-20")
