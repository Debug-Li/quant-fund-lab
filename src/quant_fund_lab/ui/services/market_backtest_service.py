from __future__ import annotations

from pathlib import Path

import pandas as pd

from quant_fund_lab.config.settings import settings
from quant_fund_lab.market.backtest.report import orders_to_frame
from quant_fund_lab.market.data.storage.market_data_repository import MarketDataRepository
from quant_fund_lab.market.services.backtest_service import make_demo_bars, run_backtest
from quant_fund_lab.market.services.strategy_service import instantiate_strategy, list_strategy_files
from quant_fund_lab.market.strategies.examples.ma_cross import Strategy as MACrossStrategy
from quant_fund_lab.ui.services.result import ServiceResult


def list_available_market_strategies_service() -> ServiceResult:
    try:
        files = list_strategy_files()
        df = pd.DataFrame({"strategy": [path.stem for path in files], "path": [str(path) for path in files]})
        return ServiceResult(True, f"已发现 {len(files)} 个策略文件", dataframe=df, data=files)
    except Exception as exc:
        return ServiceResult(False, f"读取策略列表失败: {exc}", error_detail=repr(exc))


def run_demo_ma_cross_service(initial_cash: float, commission_rate: float, slippage_rate: float) -> ServiceResult:
    try:
        result = run_backtest(make_demo_bars(), MACrossStrategy(), initial_cash, commission_rate, slippage_rate)
        payload = {"result": result, "orders": orders_to_frame(result), "equity": result.equity_curve}
        return ServiceResult(True, "MA Cross 演示回测完成", data=payload, dataframe=result.equity_curve)
    except Exception as exc:
        return ServiceResult(False, f"MA Cross 演示回测失败: {exc}", error_detail=repr(exc))


def run_market_strategy_service(
    symbol: str,
    market: str,
    start: str,
    end: str,
    strategy_name: str,
    initial_cash: float,
    commission_rate: float,
    slippage_rate: float,
) -> ServiceResult:
    try:
        repo = MarketDataRepository()
        bars = repo.get_bars(symbol=symbol, start=start, end=end, timeframe="1d")
        if bars.empty:
            return ServiceResult(False, f"未找到 {symbol} 的本地行情，请先到“看盘中心”获取数据。")

        strategy_path = Path(settings.strategy_dir) / f"{strategy_name}.py"
        strategy = instantiate_strategy(strategy_path)
        result = run_backtest(bars, strategy, initial_cash, commission_rate, slippage_rate)
        payload = {"result": result, "orders": orders_to_frame(result), "equity": result.equity_curve}
        return ServiceResult(True, f"{strategy_name} 回测完成", data=payload, dataframe=result.equity_curve)
    except Exception as exc:
        return ServiceResult(False, f"策略回测失败: {exc}", error_detail=repr(exc))
