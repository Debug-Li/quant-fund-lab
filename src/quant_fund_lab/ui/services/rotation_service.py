from __future__ import annotations

from quant_fund_lab.backtest.rotation_bt import load_price_matrix, run_backtest_with_params
from quant_fund_lab.ui.config import ROTATION_STATS_PATH
from quant_fund_lab.ui.services.result import ServiceResult


def run_rotation_backtest_service(
    lookback_days: int,
    top_n: int,
    trend_days: int,
) -> ServiceResult:
    try:
        prices = load_price_matrix()
    except FileNotFoundError as exc:
        return ServiceResult(False, "未找到 ETF close matrix，请先到“数据中心”生成演示数据或下载真实数据。", error_detail=str(exc))

    try:
        result = run_backtest_with_params(prices, lookback_days, top_n, trend_days)
        ROTATION_STATS_PATH.parent.mkdir(parents=True, exist_ok=True)
        result.stats.to_csv(ROTATION_STATS_PATH)
        return ServiceResult(
            True,
            f"轮动回测完成: lookback={lookback_days}, top_n={top_n}, trend={trend_days}",
            data=result,
            dataframe=result.stats.reset_index().rename(columns={"index": "stat"}),
            files=[ROTATION_STATS_PATH],
        )
    except Exception as exc:
        return ServiceResult(False, f"轮动回测失败: {exc}", error_detail=repr(exc))
