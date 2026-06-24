from __future__ import annotations

from fastapi import APIRouter

from quant_lab.schemas.response import ApiResponse
from quant_lab.services.demo_data_service import get_demo_dashboard
from quant_lab.services.real_data_service import get_real_dashboard


router = APIRouter()


@router.get("/overview", response_model=ApiResponse)
def overview() -> ApiResponse:
    try:
        return ApiResponse(success=True, message="real dashboard", data=get_real_dashboard())
    except Exception as exc:
        data = get_demo_dashboard()
        data["fallbackReason"] = str(exc)
        return ApiResponse(success=True, message="real dashboard unavailable, fallback to demo", data=data)
