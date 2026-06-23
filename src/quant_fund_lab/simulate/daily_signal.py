from __future__ import annotations

from pathlib import Path

import pandas as pd

from quant_fund_lab.data.akshare_loader import PROJECT_ROOT, load_universe
from quant_fund_lab.features.momentum import equal_weight_targets, momentum_score, top_n_selection, trend_mask


def load_price_matrix(path: Path | None = None) -> pd.DataFrame:
    price_path = path or PROJECT_ROOT / "data" / "processed" / "etf_close.parquet"
    if not price_path.exists():
        raise FileNotFoundError(
            f"price file not found: {price_path}. Run `uv run qfl-data` first."
        )
    return pd.read_parquet(price_path).sort_index().ffill().dropna(how="all")


def latest_signal(prices: pd.DataFrame) -> pd.DataFrame:
    config = load_universe()
    lookback_days = int(config.get("lookback_days", 60))
    top_n = int(config.get("top_n", 3))
    trend_days = int(config.get("trend_filter_days", 20))

    scores = momentum_score(prices, lookback_days=lookback_days)
    eligible = trend_mask(prices, window=trend_days)
    selected = top_n_selection(scores, top_n=top_n, eligible=eligible)
    weights = equal_weight_targets(selected)

    last_date = prices.index.max()
    table = pd.DataFrame(
        {
            "fund": prices.columns,
            "close": prices.loc[last_date],
            "momentum": scores.loc[last_date],
            "eligible": eligible.loc[last_date],
            "target_weight": weights.loc[last_date],
        }
    )
    table = table.sort_values(["target_weight", "momentum"], ascending=[False, False])
    table.insert(0, "date", last_date)
    return table


def main() -> None:
    prices = load_price_matrix()
    signal = latest_signal(prices)
    output_path = PROJECT_ROOT / "reports" / "latest_signal.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    signal.to_csv(output_path, index=False)

    print(signal.to_string(index=False))
    print(f"saved signal -> {output_path}")


if __name__ == "__main__":
    main()
