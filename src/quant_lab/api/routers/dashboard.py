from __future__ import annotations

from fastapi import APIRouter

from quant_lab.schemas.response import ApiResponse
from quant_lab.services.demo_data_service import get_demo_dashboard


router = APIRouter()


@router.get("/overview", response_model=ApiResponse)
def overview() -> ApiResponse:
    return ApiResponse(success=True, message="demo dashboard", data=get_demo_dashboard())
