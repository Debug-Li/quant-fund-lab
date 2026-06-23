from __future__ import annotations

from fastapi import APIRouter

from quant_lab.schemas.response import ApiResponse
from quant_lab.services.demo_data_service import get_demo_reports


router = APIRouter()


@router.get("/list", response_model=ApiResponse)
def list_reports() -> ApiResponse:
    return ApiResponse(success=True, data=get_demo_reports())


@router.get("/{report_id}", response_model=ApiResponse)
def get_report(report_id: str) -> ApiResponse:
    data = get_demo_reports()
    data["selected"] = report_id
    return ApiResponse(success=True, data=data)
