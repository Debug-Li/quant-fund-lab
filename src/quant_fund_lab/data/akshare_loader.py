from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import akshare as ak
import pandas as pd
import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[3]


@dataclass(frozen=True)
class Asset:
    symbol: str
    name: str
    category: str


def load_universe(path: Path | str = PROJECT_ROOT / "configs" / "universe.yml") -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def normalize_etf_hist(raw: pd.DataFrame, symbol: str, name: str) -> pd.DataFrame:
    column_map = {
        "日期": "date",
        "开盘": "open",
        "收盘": "close",
        "最高": "high",
        "最低": "low",
        "成交量": "volume",
        "成交额": "amount",
        "振幅": "amplitude",
        "涨跌幅": "pct_change",
        "涨跌额": "change",
        "换手率": "turnover",
    }
    df = raw.rename(columns=column_map).copy()
    if "date" not in df.columns or "close" not in df.columns:
        raise ValueError(f"{symbol} returned unexpected columns: {list(raw.columns)}")

    df["date"] = pd.to_datetime(df["date"])
    numeric_columns = [col for col in df.columns if col not in {"date"}]
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["symbol"] = symbol
    df["name"] = name
    return df.sort_values("date").reset_index(drop=True)


def fetch_etf_daily(
    symbol: str,
    name: str,
    start_date: str = "20200101",
    end_date: str | None = None,
    adjust: str = "qfq",
) -> pd.DataFrame:
    end = end_date or datetime.now().strftime("%Y%m%d")
    raw = ak.fund_etf_hist_em(
        symbol=symbol,
        period="daily",
        start_date=start_date,
        end_date=end,
        adjust=adjust,
    )
    return normalize_etf_hist(raw, symbol=symbol, name=name)


def fetch_universe_prices(config_path: Path | str = PROJECT_ROOT / "configs" / "universe.yml") -> pd.DataFrame:
    config = load_universe(config_path)
    frames: list[pd.DataFrame] = []
    for asset in config["assets"]:
        frame = fetch_etf_daily(
            symbol=asset["symbol"],
            name=asset["name"],
            start_date=config.get("start_date", "20200101"),
            end_date=config.get("end_date"),
            adjust=config.get("adjust", "qfq"),
        )
        frame["category"] = asset.get("category", "unknown")
        frames.append(frame)
    return pd.concat(frames, ignore_index=True)


def to_price_matrix(df: pd.DataFrame, value_column: str = "close") -> pd.DataFrame:
    matrix = df.pivot(index="date", columns="name", values=value_column).sort_index()
    return matrix.dropna(axis=1, how="all").ffill()
