from __future__ import annotations

from pathlib import Path

from quant_fund_lab.market.strategies.loader import load_strategy_class


def test_load_strategy_class_from_file() -> None:
    path = Path("strategies/ma_cross.py")
    strategy_class = load_strategy_class(path)
    strategy = strategy_class()
    assert strategy.name == "MA Cross"
