from __future__ import annotations

from pathlib import Path

from quant_fund_lab.config.settings import settings
from quant_fund_lab.market.strategies.loader import load_strategy_class


def list_strategy_files(strategy_dir: str | Path = settings.strategy_dir) -> list[Path]:
    path = Path(strategy_dir)
    path.mkdir(parents=True, exist_ok=True)
    return sorted(path.glob("*.py"))


def instantiate_strategy(path: str | Path):
    strategy_class = load_strategy_class(path)
    return strategy_class()
