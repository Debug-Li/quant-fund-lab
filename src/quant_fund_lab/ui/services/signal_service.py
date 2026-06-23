from __future__ import annotations

from quant_fund_lab.simulate.daily_signal import latest_signal, load_price_matrix
from quant_fund_lab.ui.config import LATEST_SIGNAL_PATH
from quant_fund_lab.ui.services.result import ServiceResult


def generate_latest_signal_service() -> ServiceResult:
    try:
        prices = load_price_matrix()
    except FileNotFoundError as exc:
        return ServiceResult(False, "未找到 ETF close matrix，请先到“数据中心”生成演示数据或下载真实数据。", error_detail=str(exc))

    try:
        signal = latest_signal(prices)
        LATEST_SIGNAL_PATH.parent.mkdir(parents=True, exist_ok=True)
        signal.to_csv(LATEST_SIGNAL_PATH, index=False)
        return ServiceResult(True, f"最新模拟信号已生成，共 {len(signal)} 行", dataframe=signal, data=signal, files=[LATEST_SIGNAL_PATH])
    except Exception as exc:
        return ServiceResult(False, f"生成模拟信号失败: {exc}", error_detail=repr(exc))
