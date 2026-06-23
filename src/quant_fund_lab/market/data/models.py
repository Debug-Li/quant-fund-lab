from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class MarketBar:
    symbol: str
    datetime: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
    amount: float | None = None
    adjusted_close: float | None = None
    source: str = "unknown"
    timeframe: str = "1d"


@dataclass(frozen=True)
class Order:
    order_id: str
    symbol: str
    side: str
    size: float
    price: float
    datetime: datetime
    commission: float
    slippage: float
    status: str = "FILLED"


@dataclass(frozen=True)
class Trade:
    trade_id: str
    symbol: str
    entry_dt: datetime
    exit_dt: datetime | None
    entry_price: float
    exit_price: float | None
    size: float
    pnl: float
    return_pct: float


@dataclass(frozen=True)
class PortfolioSnapshot:
    datetime: datetime
    cash: float
    market_value: float
    total_equity: float
    drawdown: float
