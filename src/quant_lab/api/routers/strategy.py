from __future__ import annotations

from fastapi import APIRouter

from quant_lab.schemas.response import ApiResponse
from quant_lab.services.demo_data_service import get_demo_strategy_lab


router = APIRouter()


@router.get("/list", response_model=ApiResponse)
def list_strategies() -> ApiResponse:
    return ApiResponse(success=True, data=get_demo_strategy_lab()["strategies"])


@router.get("/{strategy_id}", response_model=ApiResponse)
def get_strategy(strategy_id: str) -> ApiResponse:
    data = get_demo_strategy_lab()
    data["selected"] = strategy_id
    return ApiResponse(success=True, data=data)


@router.post("/{strategy_id}/validate", response_model=ApiResponse)
def validate(strategy_id: str) -> ApiResponse:
    return ApiResponse(success=True, message=f"{strategy_id} demo validation passed")
