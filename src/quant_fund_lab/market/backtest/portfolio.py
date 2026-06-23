from __future__ import annotations

from quant_fund_lab.market.data.models import PortfolioSnapshot


def snapshot(datetime, cash: float, market_value: float, peak_equity: float) -> PortfolioSnapshot:
    total_equity = cash + market_value
    drawdown = total_equity / peak_equity - 1 if peak_equity > 0 else 0.0
    return PortfolioSnapshot(datetime, cash, market_value, total_equity, drawdown)
