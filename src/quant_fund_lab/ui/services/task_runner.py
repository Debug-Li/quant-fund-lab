from __future__ import annotations

import traceback
from collections.abc import Callable
from typing import Any

from quant_fund_lab.ui.services.result import ServiceResult


def run_task(name: str, func: Callable[..., ServiceResult], *args: Any, **kwargs: Any) -> ServiceResult:
    try:
        result = func(*args, **kwargs)
        result.logs.insert(0, f"任务完成: {name}" if result.success else f"任务未完成: {name}")
        return result
    except Exception as exc:
        return ServiceResult(
            success=False,
            message=f"任务失败: {name}: {exc}",
            error_detail=traceback.format_exc(),
            logs=[f"任务失败: {name}"],
        )
