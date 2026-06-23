from __future__ import annotations

import pandas as pd

from quant_fund_lab.market.backtest.engine import BacktestResult


def orders_to_frame(result: BacktestResult) -> pd.DataFrame:
    return pd.DataFrame([order.__dict__ for order in result.orders])


def metrics_to_frame(result: BacktestResult) -> pd.DataFrame:
    return pd.DataFrame([{"metric": key, "value": value} for key, value in result.metrics.items()])
