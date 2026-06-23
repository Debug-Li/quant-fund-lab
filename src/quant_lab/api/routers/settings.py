from __future__ import annotations

from fastapi import APIRouter

from quant_lab.schemas.response import ApiResponse
from quant_lab.services.demo_data_service import get_demo_settings


router = APIRouter()


@router.get("", response_model=ApiResponse)
def get_settings() -> ApiResponse:
    return ApiResponse(success=True, data=get_demo_settings())


@router.get("/diagnostics", response_model=ApiResponse)
def diagnostics() -> ApiResponse:
    return ApiResponse(success=True, data=get_demo_settings())
