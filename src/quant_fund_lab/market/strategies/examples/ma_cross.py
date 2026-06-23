from __future__ import annotations

from quant_fund_lab.market.strategies.base import BaseStrategy, StrategyContext


class Strategy(BaseStrategy):
    name = "MA Cross"

    def init(self, context: StrategyContext) -> None:
        self.fast = 10
        self.slow = 30

    def on_bar(self, context: StrategyContext, bar) -> None:
        hist = context.history
        if len(hist) < self.slow + 1:
            return

        fast_ma = hist["close"].rolling(self.fast).mean()
        slow_ma = hist["close"].rolling(self.slow).mean()

        prev_fast = fast_ma.iloc[-2]
        prev_slow = slow_ma.iloc[-2]
        curr_fast = fast_ma.iloc[-1]
        curr_slow = slow_ma.iloc[-1]

        if context.position <= 0 and prev_fast <= prev_slow and curr_fast > curr_slow:
            context.buy(percent=1.0)
            context.log("MA golden cross, buy next open.")

        if context.position > 0 and prev_fast >= prev_slow and curr_fast < curr_slow:
            context.close()
            context.log("MA death cross, close next open.")
