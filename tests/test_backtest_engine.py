from __future__ import annotations

import pytest

from quant_fund_lab.market.backtest.engine import BacktestEngine
from quant_fund_lab.market.strategies.base import BaseStrategy, StrategyContext
from quant_fund_lab.market.strategies.examples.ma_cross import Strategy as MACrossStrategy
from quant_fund_lab.utils.exceptions import BacktestError


class BuyAndHoldStrategy(BaseStrategy):
    name = "Buy And Hold"

    def on_bar(self, context: StrategyContext, bar) -> None:
        if len(context.history) == 1 and context.position <= 0:
            context.buy(percent=1.0)


def test_backtest_engine_generates_equity_and_orders(sample_bars) -> None:
    result = BacktestEngine(initial_cash=10_000).run(sample_bars("AAA"), BuyAndHoldStrategy())

    assert not result.equity_curve.empty
    assert result.metrics["total_return"] > 0
    assert len(result.orders) >= 1
    assert result.orders[0].side == "BUY"


def test_backtest_engine_runs_ma_cross(sample_bars) -> None:
    result = BacktestEngine(initial_cash=10_000).run(sample_bars("AAA"), MACrossStrategy())
    assert result.strategy_name == "MA Cross"
    assert "sharpe" in result.metrics


def test_backtest_rejects_non_positive_prices(sample_bars) -> None:
    bars = sample_bars("AAA")
    bars.loc[0, "close"] = 0

    with pytest.raises(BacktestError):
        BacktestEngine().run(bars, BuyAndHoldStrategy())
