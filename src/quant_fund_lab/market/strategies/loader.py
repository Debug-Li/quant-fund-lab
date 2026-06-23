from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

from quant_fund_lab.utils.exceptions import StrategyLoadError


def load_strategy_module(path: str | Path) -> ModuleType:
    strategy_path = Path(path)
    if not strategy_path.exists():
        raise StrategyLoadError(f"Strategy file not found: {strategy_path}")

    spec = importlib.util.spec_from_file_location(strategy_path.stem, strategy_path)
    if spec is None or spec.loader is None:
        raise StrategyLoadError(f"Cannot import strategy file: {strategy_path}")

    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception as exc:
        raise StrategyLoadError(f"Strategy import failed: {strategy_path}: {exc}") from exc
    return module


def load_strategy_class(path: str | Path) -> type:
    module = load_strategy_module(path)
    strategy_class = getattr(module, "Strategy", None)
    if strategy_class is None:
        raise StrategyLoadError("Strategy file must define class Strategy")
    return strategy_class
