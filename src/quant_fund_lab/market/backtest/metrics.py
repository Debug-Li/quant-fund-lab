from __future__ import annotations

import math

import pandas as pd

from quant_fund_lab.market.data.models import Order, PortfolioSnapshot


def calculate_metrics(snapshots: list[PortfolioSnapshot], orders: list[Order]) -> dict[str, float]:
    if not snapshots:
        return {
            "total_return": 0.0,
            "annual_return": 0.0,
            "max_drawdown": 0.0,
            "sharpe": 0.0,
            "win_rate": 0.0,
            "profit_loss_ratio": 0.0,
            "trade_count": 0.0,
            "avg_holding_days": 0.0,
        }

    equity = pd.Series(
        [item.total_equity for item in snapshots],
        index=pd.to_datetime([item.datetime for item in snapshots]),
        dtype="float64",
    )
    returns = equity.pct_change(fill_method=None).dropna()
    total_return = equity.iloc[-1] / equity.iloc[0] - 1
    days = max((equity.index[-1] - equity.index[0]).days, 1)
    annual_return = (1 + total_return) ** (365 / days) - 1
    drawdown = equity / equity.cummax() - 1
    max_drawdown = float(drawdown.min())
    sharpe = 0.0
    if not returns.empty and returns.std() != 0:
        sharpe = float(math.sqrt(252) * returns.mean() / returns.std())

    closed_trade_returns = _closed_trade_returns(orders)
    wins = [ret for ret in closed_trade_returns if ret > 0]
    losses = [ret for ret in closed_trade_returns if ret <= 0]
    win_rate = len(wins) / len(closed_trade_returns) if closed_trade_returns else 0.0
    profit_loss_ratio = abs(sum(wins) / len(wins) / (sum(losses) / len(losses))) if wins and losses else 0.0

    return {
        "total_return": float(total_return),
        "annual_return": float(annual_return),
        "max_drawdown": max_drawdown,
        "sharpe": sharpe,
        "win_rate": float(win_rate),
        "profit_loss_ratio": float(profit_loss_ratio),
        "trade_count": float(len([order for order in orders if order.side == "SELL"])),
        "avg_holding_days": float(_avg_holding_days(orders)),
    }


def _closed_trade_returns(orders: list[Order]) -> list[float]:
    returns: list[float] = []
    entry_price = None
    for order in orders:
        if order.side == "BUY":
            entry_price = order.price
        elif order.side == "SELL" and entry_price:
            returns.append(order.price / entry_price - 1)
            entry_price = None
    return returns


def _avg_holding_days(orders: list[Order]) -> float:
    holding_days: list[int] = []
    entry_dt = None
    for order in orders:
        if order.side == "BUY":
            entry_dt = order.datetime
        elif order.side == "SELL" and entry_dt is not None:
            holding_days.append(max((order.datetime - entry_dt).days, 0))
            entry_dt = None
    return sum(holding_days) / len(holding_days) if holding_days else 0.0
