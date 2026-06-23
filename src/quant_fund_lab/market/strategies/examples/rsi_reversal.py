from __future__ import annotations

from quant_fund_lab.market.indicators.rsi import rsi
from quant_fund_lab.market.strategies.base import BaseStrategy, StrategyContext


class Strategy(BaseStrategy):
    name = "RSI Reversal"

    def init(self, context: StrategyContext) -> None:
        self.window = 14
        self.buy_threshold = 30
        self.sell_threshold = 60

    def on_bar(self, context: StrategyContext, bar) -> None:
        hist = context.history
        if len(hist) < self.window + 1:
            return

        current_rsi = rsi(hist, window=self.window).iloc[-1]
        if context.position <= 0 and current_rsi < self.buy_threshold:
            context.buy(percent=1.0)
            context.log("RSI oversold, buy next open.")
        elif context.position > 0 and current_rsi > self.sell_threshold:
            context.close()
            context.log("RSI recovered, close next open.")
