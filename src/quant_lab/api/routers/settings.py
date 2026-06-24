from __future__ import annotations

from fastapi import APIRouter

from quant_lab.schemas.response import ApiResponse
from quant_lab.services.demo_data_service import get_demo_settings
from quant_lab.services.real_data_service import get_real_settings


router = APIRouter()


@router.get("", response_model=ApiResponse)
def get_settings() -> ApiResponse:
    try:
        return ApiResponse(success=True, data=get_real_settings())
    except Exception as exc:
        data = get_demo_settings()
        data["fallbackReason"] = str(exc)
        return ApiResponse(success=True, message="real settings unavailable, fallback to demo", data=data)


@router.get("/diagnostics", response_model=ApiResponse)
def diagnostics() -> ApiResponse:
    try:
        return ApiResponse(success=True, data=get_real_settings())
    except Exception as exc:
        data = get_demo_settings()
        data["fallbackReason"] = str(exc)
        return ApiResponse(success=True, message="real diagnostics unavailable, fallback to demo", data=data)
