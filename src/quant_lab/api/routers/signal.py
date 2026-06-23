from __future__ import annotations

from fastapi import APIRouter

from quant_lab.schemas.response import ApiResponse
from quant_lab.services.demo_data_service import get_demo_signals


router = APIRouter()


@router.get("/list", response_model=ApiResponse)
def list_signals() -> ApiResponse:
    return ApiResponse(success=True, data=get_demo_signals())


@router.post("/generate", response_model=ApiResponse)
def generate() -> ApiResponse:
    return ApiResponse(success=True, message="demo signals generated", data=get_demo_signals())
