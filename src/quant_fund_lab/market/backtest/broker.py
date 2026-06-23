from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4

import pandas as pd

from quant_fund_lab.market.data.models import Order
from quant_fund_lab.market.strategies.base import OrderRequest


@dataclass
class Broker:
    cash: float
    commission_rate: float = 0.0003
    slippage_rate: float = 0.0002
    position: float = 0.0
    orders: list[Order] = field(default_factory=list)

    def market_value(self, price: float) -> float:
        return self.position * price

    def total_equity(self, price: float) -> float:
        return self.cash + self.market_value(price)

    def execute(self, request: OrderRequest, bar: pd.Series, symbol: str) -> Order | None:
        side = request.side
        price = float(bar["open"])
        if price <= 0:
            return None

        if side == "CLOSE":
            if self.position <= 0:
                return None
            return self._sell(size=self.position, price=price, bar=bar, symbol=symbol)

        if side == "BUY":
            size = request.size
            if size is None:
                percent = request.percent if request.percent is not None else 1.0
                spendable = max(0.0, self.cash * min(percent, 1.0))
                execution_price = price * (1 + self.slippage_rate)
                size = spendable / (execution_price * (1 + self.commission_rate))
            return self._buy(size=size, price=price, bar=bar, symbol=symbol)

        if side == "SELL":
            size = request.size
            if size is None:
                percent = request.percent if request.percent is not None else 1.0
                size = self.position * min(percent, 1.0)
            return self._sell(size=size, price=price, bar=bar, symbol=symbol)

        return None

    def _buy(self, size: float, price: float, bar: pd.Series, symbol: str) -> Order | None:
        if size <= 0:
            return None
        execution_price = price * (1 + self.slippage_rate)
        gross = size * execution_price
        commission = gross * self.commission_rate
        total_cost = gross + commission
        if total_cost > self.cash:
            size = self.cash / (execution_price * (1 + self.commission_rate))
            gross = size * execution_price
            commission = gross * self.commission_rate
            total_cost = gross + commission
        if size <= 0 or total_cost > self.cash + 1e-8:
            return None
        self.cash -= total_cost
        self.position += size
        order = Order(str(uuid4()), symbol, "BUY", size, execution_price, bar["datetime"], commission, execution_price - price)
        self.orders.append(order)
        return order

    def _sell(self, size: float, price: float, bar: pd.Series, symbol: str) -> Order | None:
        size = min(size, self.position)
        if size <= 0:
            return None
        execution_price = price * (1 - self.slippage_rate)
        gross = size * execution_price
        commission = gross * self.commission_rate
        self.cash += gross - commission
        self.position -= size
        order = Order(str(uuid4()), symbol, "SELL", size, execution_price, bar["datetime"], commission, price - execution_price)
        self.orders.append(order)
        return order
