from __future__ import annotations

import numpy as np
import pandas as pd

from quant_fund_lab.data.akshare_loader import PROJECT_ROOT, fetch_universe_prices, load_universe, to_price_matrix


def save_price_data(raw_prices: pd.DataFrame, price_matrix: pd.DataFrame) -> None:
    raw_path = PROJECT_ROOT / "data" / "raw" / "etf_daily.parquet"
    processed_path = PROJECT_ROOT / "data" / "processed" / "etf_close.parquet"

    raw_path.parent.mkdir(parents=True, exist_ok=True)
    processed_path.parent.mkdir(parents=True, exist_ok=True)
    raw_prices.to_parquet(raw_path, index=False)
    price_matrix.to_parquet(processed_path)

    print(f"saved raw rows: {len(raw_prices):,} -> {raw_path}")
    print(f"saved close matrix: {price_matrix.shape} -> {processed_path}")


def build_demo_prices() -> tuple[pd.DataFrame, pd.DataFrame]:
    config = load_universe()
    assets = config["assets"]
    dates = pd.bdate_range("2020-01-02", periods=900)
    rng = np.random.default_rng(42)

    raw_frames: list[pd.DataFrame] = []
    close_frames: dict[str, pd.Series] = {}
    market = rng.normal(0.00025, 0.009, len(dates))

    for index, asset in enumerate(assets):
        drift = 0.00005 + index * 0.000015
        volatility = 0.010 + (index % 4) * 0.002
        cycle = np.sin(np.linspace(0, 10, len(dates)) + index) * 0.0015
        returns = drift + 0.45 * market + cycle + rng.normal(0, volatility, len(dates))
        close = 100 * np.exp(np.cumsum(returns))
        open_ = close * (1 + rng.normal(0, 0.002, len(dates)))
        high = np.maximum(open_, close) * (1 + np.abs(rng.normal(0, 0.003, len(dates))))
        low = np.minimum(open_, close) * (1 - np.abs(rng.normal(0, 0.003, len(dates))))

        frame = pd.DataFrame(
            {
                "date": dates,
                "open": open_,
                "close": close,
                "high": high,
                "low": low,
                "volume": rng.integers(5_000_000, 50_000_000, len(dates)),
                "amount": rng.integers(50_000_000, 500_000_000, len(dates)),
                "symbol": asset["symbol"],
                "name": asset["name"],
                "category": asset.get("category", "unknown"),
            }
        )
        raw_frames.append(frame)
        close_frames[asset["name"]] = pd.Series(close, index=dates)

    raw_prices = pd.concat(raw_frames, ignore_index=True)
    price_matrix = pd.DataFrame(close_frames).sort_index()
    return raw_prices, price_matrix


def demo_main() -> None:
    raw_prices, price_matrix = build_demo_prices()
    save_price_data(raw_prices, price_matrix)
    print("demo data generated. Replace with `uv run qfl-data` when live data access is available.")


def main() -> None:
    prices = fetch_universe_prices()
    price_matrix = to_price_matrix(prices)
    save_price_data(prices, price_matrix)


if __name__ == "__main__":
    main()
