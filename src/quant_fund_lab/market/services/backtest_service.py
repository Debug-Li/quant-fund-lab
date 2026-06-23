from __future__ import annotations

import numpy as np
import pandas as pd

from quant_fund_lab.market.backtest.engine import BacktestEngine, BacktestResult
from quant_fund_lab.market.strategies.examples.ma_cross import Strategy as MACrossStrategy


def make_demo_bars(symbol: str = "DEMO") -> pd.DataFrame:
    dates = pd.bdate_range("2022-01-03", periods=260)
    trend = np.linspace(0, 0.28, len(dates))
    cycle = np.sin(np.linspace(0, 14, len(dates))) * 0.08
    close = 100 * (1 + trend + cycle)
    open_ = close * (1 + np.sin(np.linspace(0, 8, len(dates))) * 0.002)
    high = np.maximum(open_, close) * 1.01
    low = np.minimum(open_, close) * 0.99
    return pd.DataFrame(
        {
            "symbol": symbol,
            "datetime": dates,
            "open": open_,
            "high": high,
            "low": low,
            "close": close,
            "volume": 1_000_000,
        }
    )


def run_backtest(
    data: pd.DataFrame,
    strategy,
    initial_cash: float = 100_000.0,
    commission_rate: float = 0.0003,
    slippage_rate: float = 0.0002,
) -> BacktestResult:
    engine = BacktestEngine(
        initial_cash=initial_cash,
        commission_rate=commission_rate,
        slippage_rate=slippage_rate,
    )
    return engine.run(data=data, strategy=strategy)


def run_example_backtest() -> BacktestResult:
    return run_backtest(make_demo_bars(), MACrossStrategy())


def main() -> None:
    result = run_example_backtest()
    for metric, value in result.metrics.items():
        print(f"{metric}: {value:.6f}")
    print(f"orders: {len(result.orders)}")
