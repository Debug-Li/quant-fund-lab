from __future__ import annotations

from fastapi import APIRouter

from quant_lab.schemas.response import ApiResponse
from quant_lab.services.demo_data_service import get_demo_data_center
from quant_lab.services.real_data_service import download_real_dataset, generate_demo_dataset, get_real_data_center


router = APIRouter()


@router.get("/status", response_model=ApiResponse)
def status() -> ApiResponse:
    try:
        return ApiResponse(success=True, message="real data status", data=get_real_data_center())
    except Exception as exc:
        data = get_demo_data_center()
        data["fallbackReason"] = str(exc)
        return ApiResponse(success=True, message="real data status unavailable, fallback to demo", data=data)


@router.post("/demo", response_model=ApiResponse)
def demo() -> ApiResponse:
    try:
        return ApiResponse(success=True, message="demo ETF dataset generated", data=generate_demo_dataset())
    except Exception as exc:
        data = get_demo_data_center()
        data["fallbackReason"] = str(exc)
        return ApiResponse(success=True, message="demo generation failed, fallback to static demo", data=data)


@router.post("/download", response_model=ApiResponse)
def download() -> ApiResponse:
    try:
        return ApiResponse(success=True, message="real AKShare ETF dataset downloaded", data=download_real_dataset())
    except Exception as exc:
        data = get_demo_data_center()
        data["fallbackReason"] = str(exc)
        return ApiResponse(success=True, message="real download failed, fallback to demo status", data=data)


@router.get("/preview", response_model=ApiResponse)
def preview() -> ApiResponse:
    try:
        return ApiResponse(success=True, data=get_real_data_center()["datasets"])
    except Exception as exc:
        return ApiResponse(success=True, message=f"fallback to demo: {exc}", data=get_demo_data_center()["datasets"])


@router.post("/quality-check", response_model=ApiResponse)
def quality_check() -> ApiResponse:
    try:
        return ApiResponse(success=True, data=get_real_data_center()["quality"])
    except Exception as exc:
        return ApiResponse(success=True, message=f"fallback to demo: {exc}", data=get_demo_data_center()["quality"])
