from __future__ import annotations

from fastapi import APIRouter

from quant_lab.schemas.response import ApiResponse
from quant_lab.services.demo_data_service import get_demo_signals
from quant_lab.services.real_data_service import get_real_signals


router = APIRouter()


@router.get("/list", response_model=ApiResponse)
def list_signals() -> ApiResponse:
    try:
        return ApiResponse(success=True, message="real signals", data=get_real_signals())
    except Exception as exc:
        data = get_demo_signals()
        data["fallbackReason"] = str(exc)
        return ApiResponse(success=True, message="real signals unavailable, fallback to demo", data=data)


@router.post("/generate", response_model=ApiResponse)
def generate() -> ApiResponse:
    try:
        return ApiResponse(success=True, message="real signals generated", data=get_real_signals())
    except Exception as exc:
        data = get_demo_signals()
        data["fallbackReason"] = str(exc)
        return ApiResponse(success=True, message="real signals unavailable, fallback to demo", data=data)
