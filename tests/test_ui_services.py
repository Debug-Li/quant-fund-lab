from __future__ import annotations

from pathlib import Path

from quant_fund_lab.ui.services.fund_data_service import generate_demo_data_service
from quant_fund_lab.ui.services.market_backtest_service import run_demo_ma_cross_service
from quant_fund_lab.ui.services.result import ServiceResult
from quant_fund_lab.ui.services.task_runner import run_task


def test_service_result_shape() -> None:
    result = ServiceResult(success=True, message="ok")
    assert result.success is True
    assert result.message == "ok"
    assert result.files == []


def test_run_task_catches_exceptions() -> None:
    def bad_task() -> ServiceResult:
        raise RuntimeError("boom")

    result = run_task("bad", bad_task)
    assert result.success is False
    assert "boom" in result.message
    assert result.error_detail


def test_generate_demo_data_service_succeeds() -> None:
    result = generate_demo_data_service()
    assert result.success is True
    assert result.dataframe is not None
    assert len(result.files) == 2
    assert all(Path(path).exists() for path in result.files)


def test_market_backtest_demo_succeeds() -> None:
    result = run_demo_ma_cross_service(100000, 0.0003, 0.0002)
    assert result.success is True
    assert result.data["result"].metrics["trade_count"] >= 0
    assert result.data["orders"] is not None
