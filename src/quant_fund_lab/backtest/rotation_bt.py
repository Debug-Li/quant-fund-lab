from __future__ import annotations

from pathlib import Path

import bt
import pandas as pd

from quant_fund_lab.data.akshare_loader import PROJECT_ROOT, load_universe
from quant_fund_lab.features.momentum import momentum_score, top_n_selection, trend_mask


def load_price_matrix(path: Path | None = None) -> pd.DataFrame:
    price_path = path or PROJECT_ROOT / "data" / "processed" / "etf_close.parquet"
    if not price_path.exists():
        raise FileNotFoundError(
            f"price file not found: {price_path}. Run `uv run qfl-data` first."
        )
    return pd.read_parquet(price_path).sort_index().ffill().dropna(how="all")


def build_strategy(prices: pd.DataFrame, lookback_days: int, top_n: int, trend_days: int) -> bt.Strategy:
    scores = momentum_score(prices, lookback_days=lookback_days)
    eligible = trend_mask(prices, window=trend_days)
    selected = top_n_selection(scores, top_n=top_n, eligible=eligible)

    return bt.Strategy(
        "momentum_rotation",
        [
            bt.algos.RunMonthly(),
            bt.algos.SelectWhere(selected),
            bt.algos.WeighEqually(),
            bt.algos.Rebalance(),
        ],
    )


def run_backtest(prices: pd.DataFrame) -> bt.backtest.Result:
    config = load_universe()
    strategy = build_strategy(
        prices=prices,
        lookback_days=int(config.get("lookback_days", 60)),
        top_n=int(config.get("top_n", 3)),
        trend_days=int(config.get("trend_filter_days", 20)),
    )
    test = bt.Backtest(strategy, prices)
    return bt.run(test)


def run_backtest_with_params(
    prices: pd.DataFrame,
    lookback_days: int = 60,
    top_n: int = 3,
    trend_days: int = 20,
) -> bt.backtest.Result:
    strategy = build_strategy(
        prices=prices,
        lookback_days=lookback_days,
        top_n=top_n,
        trend_days=trend_days,
    )
    test = bt.Backtest(strategy, prices)
    return bt.run(test)


def main() -> None:
    prices = load_price_matrix()
    result = run_backtest(prices)

    report_dir = PROJECT_ROOT / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    stats_path = report_dir / "rotation_stats.csv"
    result.stats.to_csv(stats_path)

    result.display()
    print(f"saved stats -> {stats_path}")


if __name__ == "__main__":
    main()
