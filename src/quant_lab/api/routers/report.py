from __future__ import annotations

from fastapi import APIRouter

from quant_lab.schemas.response import ApiResponse
from quant_lab.services.demo_data_service import get_demo_reports
from quant_lab.services.real_data_service import get_real_report, get_real_reports


router = APIRouter()


@router.get("/list", response_model=ApiResponse)
def list_reports() -> ApiResponse:
    try:
        return ApiResponse(success=True, message="real reports", data=get_real_reports())
    except Exception as exc:
        data = get_demo_reports()
        data["fallbackReason"] = str(exc)
        return ApiResponse(success=True, message="real reports unavailable, fallback to demo", data=data)


@router.get("/{report_id}", response_model=ApiResponse)
def get_report(report_id: str) -> ApiResponse:
    try:
        return ApiResponse(success=True, data=get_real_report(report_id))
    except Exception as exc:
        data = get_demo_reports()
        data["selected"] = report_id
        data["fallbackReason"] = str(exc)
        return ApiResponse(success=True, message="real report unavailable, fallback to demo", data=data)
