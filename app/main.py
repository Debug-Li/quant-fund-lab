from __future__ import annotations

from quant_fund_lab.market.services.backtest_service import run_example_backtest
from quant_fund_lab.utils.logger import get_logger


logger = get_logger(__name__)


def main() -> None:
    """Start the local market research application core."""
    logger.info("Quant Fund Lab market core started.")
    result = run_example_backtest()
    logger.info(
        "Example MA backtest finished: total_return=%.2f%% max_drawdown=%.2f%% trades=%s",
        result.metrics["total_return"] * 100,
        result.metrics["max_drawdown"] * 100,
        result.metrics["trade_count"],
    )


if __name__ == "__main__":
    main()
