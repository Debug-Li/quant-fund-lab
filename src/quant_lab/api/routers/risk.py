from __future__ import annotations

from fastapi import APIRouter

from quant_lab.schemas.response import ApiResponse
from quant_lab.services.demo_data_service import get_demo_risk
from quant_lab.services.real_data_service import get_real_risk


router = APIRouter()


@router.get("/overview", response_model=ApiResponse)
def overview() -> ApiResponse:
    try:
        return ApiResponse(success=True, message="real risk", data=get_real_risk())
    except Exception as exc:
        data = get_demo_risk()
        data["fallbackReason"] = str(exc)
        return ApiResponse(success=True, message="real risk unavailable, fallback to demo", data=data)


@router.get("/alerts", response_model=ApiResponse)
def alerts() -> ApiResponse:
    try:
        return ApiResponse(success=True, data=get_real_risk()["alerts"])
    except Exception as exc:
        return ApiResponse(success=True, message=f"fallback to demo: {exc}", data=get_demo_risk()["alerts"])


@router.post("/check", response_model=ApiResponse)
def check() -> ApiResponse:
    try:
        return ApiResponse(success=True, message="real risk check completed", data=get_real_risk())
    except Exception as exc:
        data = get_demo_risk()
        data["fallbackReason"] = str(exc)
        return ApiResponse(success=True, message="real risk unavailable, fallback to demo", data=data)
