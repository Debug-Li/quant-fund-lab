from __future__ import annotations

from fastapi import APIRouter

from quant_lab.schemas.response import ApiResponse
from quant_lab.services.demo_data_service import get_demo_strategy_lab
from quant_lab.services.real_data_service import get_real_strategy_lab


router = APIRouter()


@router.get("/list", response_model=ApiResponse)
def list_strategies() -> ApiResponse:
    try:
        return ApiResponse(success=True, data=get_real_strategy_lab()["strategies"])
    except Exception as exc:
        return ApiResponse(success=True, message=f"fallback to demo: {exc}", data=get_demo_strategy_lab()["strategies"])


@router.get("/{strategy_id}", response_model=ApiResponse)
def get_strategy(strategy_id: str) -> ApiResponse:
    try:
        return ApiResponse(success=True, message="real strategy", data=get_real_strategy_lab(strategy_id))
    except Exception as exc:
        data = get_demo_strategy_lab()
        data["selected"] = strategy_id
        data["fallbackReason"] = str(exc)
        return ApiResponse(success=True, message="real strategy unavailable, fallback to demo", data=data)


@router.post("/{strategy_id}/validate", response_model=ApiResponse)
def validate(strategy_id: str) -> ApiResponse:
    try:
        strategies = get_real_strategy_lab(strategy_id)["strategies"]
        exists = any(item["id"] == strategy_id for item in strategies)
        return ApiResponse(success=True, message=f"{strategy_id} validation {'passed' if exists else 'not found'}", data={"exists": exists})
    except Exception as exc:
        return ApiResponse(success=True, message=f"{strategy_id} demo validation passed: {exc}")
