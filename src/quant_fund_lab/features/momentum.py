from __future__ import annotations

import pandas as pd


def daily_returns(prices: pd.DataFrame) -> pd.DataFrame:
    return prices.pct_change(fill_method=None).fillna(0.0)


def momentum_score(prices: pd.DataFrame, lookback_days: int = 60) -> pd.DataFrame:
    return prices.pct_change(lookback_days, fill_method=None)


def trend_mask(prices: pd.DataFrame, window: int = 20) -> pd.DataFrame:
    moving_average = prices.rolling(window).mean()
    return prices > moving_average


def top_n_selection(scores: pd.DataFrame, top_n: int = 3, eligible: pd.DataFrame | None = None) -> pd.DataFrame:
    ranked = scores.rank(axis=1, ascending=False, method="first")
    selected = ranked <= top_n
    if eligible is not None:
        selected = selected & eligible.reindex_like(selected).fillna(False)
    return selected.fillna(False)


def equal_weight_targets(selection: pd.DataFrame) -> pd.DataFrame:
    counts = selection.sum(axis=1).replace(0, pd.NA)
    weights = selection.astype(float).div(counts, axis=0).fillna(0.0)
    return weights


def max_drawdown(series: pd.Series) -> float:
    wealth = (1 + series).cumprod()
    drawdown = wealth / wealth.cummax() - 1
    return float(drawdown.min())
