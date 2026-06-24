from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Body

from quant_lab.schemas.response import ApiResponse
from quant_lab.services.demo_data_service import get_demo_backtest
from quant_lab.services.real_data_service import DEFAULT_MARKET, DEFAULT_SYMBOL, get_real_backtest


router = APIRouter()


@router.post("/run", response_model=ApiResponse)
def run_backtest_api(payload: dict[str, Any] | None = Body(default=None)) -> ApiResponse:
    params = payload or {}
    try:
        data = get_real_backtest(
            symbol=str(params.get("symbol", DEFAULT_SYMBOL)),
            market=str(params.get("market", DEFAULT_MARKET)),
            live=bool(params.get("live", False)),
            initial_cash=float(params.get("initial_cash", 100_000.0)),
            commission_rate=float(params.get("commission_rate", 0.0003)),
            slippage_rate=float(params.get("slippage_rate", 0.0002)),
        )
        return ApiResponse(success=True, message="real backtest completed", data=data)
    except Exception as exc:
        data = get_demo_backtest()
        data["fallbackReason"] = str(exc)
        return ApiResponse(success=True, message="real backtest unavailable, fallback to demo", data=data)


@router.post("/optimize", response_model=ApiResponse)
def optimize() -> ApiResponse:
    try:
        return ApiResponse(success=True, message="real optimize proxy completed", data=get_real_backtest()["optimization"])
    except Exception as exc:
        return ApiResponse(success=True, message=f"fallback to demo: {exc}", data=get_demo_backtest()["optimization"])


@router.get("/history", response_model=ApiResponse)
def history() -> ApiResponse:
    return ApiResponse(success=True, data=[{"id": "latest-real-ma-cross", "strategy": "MA Cross ETF", "createdAt": "latest"}])


@router.get("/result/{backtest_id}", response_model=ApiResponse)
def result(backtest_id: str) -> ApiResponse:
    try:
        data = get_real_backtest()
    except Exception as exc:
        data = get_demo_backtest()
        data["fallbackReason"] = str(exc)
    data["id"] = backtest_id
    return ApiResponse(success=True, data=data)
