from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from quant_fund_lab.market.backtest.broker import Broker
from quant_fund_lab.market.backtest.metrics import calculate_metrics
from quant_fund_lab.market.backtest.portfolio import snapshot
from quant_fund_lab.market.data.models import Order, PortfolioSnapshot
from quant_fund_lab.market.strategies.base import StrategyContext
from quant_fund_lab.utils.exceptions import BacktestError


@dataclass(frozen=True)
class BacktestResult:
    strategy_name: str
    symbol: str
    metrics: dict[str, float]
    orders: list[Order]
    equity_curve: pd.DataFrame
    logs: list[str]


class BacktestEngine:
    def __init__(
        self,
        initial_cash: float = 100_000.0,
        commission_rate: float = 0.0003,
        slippage_rate: float = 0.0002,
    ) -> None:
        self.initial_cash = initial_cash
        self.commission_rate = commission_rate
        self.slippage_rate = slippage_rate

    def run(self, data: pd.DataFrame, strategy, symbol: str | None = None) -> BacktestResult:
        bars = self._prepare_data(data)
        if bars.empty:
            raise BacktestError("Backtest data is empty.")

        symbol_value = symbol or str(bars["symbol"].iloc[0])
        broker = Broker(
            cash=self.initial_cash,
            commission_rate=self.commission_rate,
            slippage_rate=self.slippage_rate,
        )
        context = StrategyContext(cash=self.initial_cash, symbol=symbol_value)
        strategy.init(context)

        pending_orders = []
        snapshots: list[PortfolioSnapshot] = []
        peak_equity = self.initial_cash

        for index, bar in bars.iterrows():
            for request in pending_orders:
                broker.execute(request, bar, symbol_value)
            pending_orders = []

            context.cash = broker.cash
            context.position = broker.position
            context.current_dt = bar["datetime"]
            context.history = bars.iloc[: index + 1].copy()

            strategy.on_bar(context, bar)
            pending_orders = context.pop_orders()

            market_value = broker.market_value(float(bar["close"]))
            equity = broker.cash + market_value
            peak_equity = max(peak_equity, equity)
            snapshots.append(snapshot(bar["datetime"], broker.cash, market_value, peak_equity))

        if broker.position > 0:
            last_bar = bars.iloc[-1].copy()
            last_bar["open"] = last_bar["close"]
            broker.execute(context.close() or context.pop_orders()[0], last_bar, symbol_value)

        metrics = calculate_metrics(snapshots, broker.orders)
        equity_curve = pd.DataFrame([item.__dict__ for item in snapshots])
        return BacktestResult(
            strategy_name=getattr(strategy, "name", strategy.__class__.__name__),
            symbol=symbol_value,
            metrics=metrics,
            orders=broker.orders,
            equity_curve=equity_curve,
            logs=context.logs,
        )

    def _prepare_data(self, data: pd.DataFrame) -> pd.DataFrame:
        required = {"datetime", "open", "high", "low", "close"}
        missing = required - set(data.columns)
        if missing:
            raise BacktestError(f"Backtest data missing columns: {sorted(missing)}")
        bars = data.copy()
        bars["datetime"] = pd.to_datetime(bars["datetime"])
        if "volume" not in bars:
            bars["volume"] = 0.0
        if "symbol" not in bars:
            bars["symbol"] = "UNKNOWN"
        bars = bars.sort_values("datetime").reset_index(drop=True)
        price_columns = ["open", "high", "low", "close"]
        bars = bars.dropna(subset=price_columns)
        if (bars[price_columns] <= 0).any().any():
            raise BacktestError("Backtest data contains non-positive prices.")
        return bars
