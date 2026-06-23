from __future__ import annotations

from fastapi import APIRouter

from quant_lab.schemas.response import ApiResponse
from quant_lab.services.demo_data_service import get_demo_risk


router = APIRouter()


@router.get("/overview", response_model=ApiResponse)
def overview() -> ApiResponse:
    return ApiResponse(success=True, data=get_demo_risk())


@router.get("/alerts", response_model=ApiResponse)
def alerts() -> ApiResponse:
    return ApiResponse(success=True, data=get_demo_risk()["alerts"])


@router.post("/check", response_model=ApiResponse)
def check() -> ApiResponse:
    return ApiResponse(success=True, message="demo risk check completed", data=get_demo_risk())
