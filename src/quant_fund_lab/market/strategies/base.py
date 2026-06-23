from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import pandas as pd


OrderSide = Literal["BUY", "SELL", "CLOSE"]


@dataclass(frozen=True)
class OrderRequest:
    side: OrderSide
    size: float | None = None
    percent: float | None = None


class StrategyContext:
    def __init__(self, cash: float, symbol: str) -> None:
        self.cash = cash
        self.position = 0.0
        self.symbol = symbol
        self.current_dt = None
        self.history = pd.DataFrame()
        self.logs: list[str] = []
        self._orders: list[OrderRequest] = []

    def buy(self, size: float | None = None, percent: float | None = None) -> None:
        self._orders.append(OrderRequest("BUY", size=size, percent=percent))

    def sell(self, size: float | None = None, percent: float | None = None) -> None:
        self._orders.append(OrderRequest("SELL", size=size, percent=percent))

    def close(self) -> None:
        self._orders.append(OrderRequest("CLOSE"))

    def log(self, message: str) -> None:
        self.logs.append(f"{self.current_dt}: {message}")

    def pop_orders(self) -> list[OrderRequest]:
        orders = self._orders
        self._orders = []
        return orders


class BaseStrategy:
    name = "Base Strategy"

    def init(self, context: StrategyContext) -> None:
        """Initialize strategy state."""

    def on_bar(self, context: StrategyContext, bar: pd.Series) -> None:
        """Run strategy logic after the current bar closes."""
