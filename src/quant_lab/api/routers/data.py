from __future__ import annotations

from fastapi import APIRouter

from quant_lab.schemas.response import ApiResponse
from quant_lab.services.demo_data_service import get_demo_data_center


router = APIRouter()


@router.get("/status", response_model=ApiResponse)
def status() -> ApiResponse:
    return ApiResponse(success=True, data=get_demo_data_center())


@router.post("/demo", response_model=ApiResponse)
def demo() -> ApiResponse:
    return ApiResponse(success=True, message="demo data ready", data=get_demo_data_center())


@router.get("/preview", response_model=ApiResponse)
def preview() -> ApiResponse:
    return ApiResponse(success=True, data=get_demo_data_center()["datasets"])


@router.post("/quality-check", response_model=ApiResponse)
def quality_check() -> ApiResponse:
    return ApiResponse(success=True, data=get_demo_data_center()["quality"])
