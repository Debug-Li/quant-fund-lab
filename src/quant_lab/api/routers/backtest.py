from __future__ import annotations

from fastapi import APIRouter

from quant_lab.schemas.response import ApiResponse
from quant_lab.services.demo_data_service import get_demo_backtest


router = APIRouter()


@router.post("/run", response_model=ApiResponse)
def run_backtest() -> ApiResponse:
    return ApiResponse(success=True, message="demo backtest completed", data=get_demo_backtest())


@router.post("/optimize", response_model=ApiResponse)
def optimize() -> ApiResponse:
    return ApiResponse(success=True, message="demo optimize completed", data=get_demo_backtest()["optimization"])


@router.get("/history", response_model=ApiResponse)
def history() -> ApiResponse:
    return ApiResponse(success=True, data=[{"id": "demo-bt-001", "strategy": "MA 动量轮动", "createdAt": "2026-06-23 14:30"}])


@router.get("/result/{backtest_id}", response_model=ApiResponse)
def result(backtest_id: str) -> ApiResponse:
    data = get_demo_backtest()
    data["id"] = backtest_id
    return ApiResponse(success=True, data=data)
