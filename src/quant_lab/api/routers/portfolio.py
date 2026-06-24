from __future__ import annotations

from fastapi import APIRouter

from quant_lab.schemas.response import ApiResponse
from quant_lab.services.demo_data_service import get_demo_portfolio
from quant_lab.services.real_data_service import get_real_portfolio


router = APIRouter()


@router.get("/overview", response_model=ApiResponse)
def overview() -> ApiResponse:
    try:
        return ApiResponse(success=True, message="real portfolio", data=get_real_portfolio())
    except Exception as exc:
        data = get_demo_portfolio()
        data["fallbackReason"] = str(exc)
        return ApiResponse(success=True, message="real portfolio unavailable, fallback to demo", data=data)


@router.get("/holdings", response_model=ApiResponse)
def holdings() -> ApiResponse:
    try:
        return ApiResponse(success=True, data=get_real_portfolio()["holdings"])
    except Exception as exc:
        return ApiResponse(success=True, message=f"fallback to demo: {exc}", data=get_demo_portfolio()["holdings"])


@router.get("/risk", response_model=ApiResponse)
def risk() -> ApiResponse:
    try:
        data = get_real_portfolio()
    except Exception as exc:
        data = get_demo_portfolio()
        data["fallbackReason"] = str(exc)
    return ApiResponse(success=True, data={"factorExposure": data["factorExposure"], "correlation": data["correlation"], "riskContribution": data["riskContribution"]})


@router.get("/rebalance/suggestion", response_model=ApiResponse)
def rebalance_suggestion() -> ApiResponse:
    try:
        return ApiResponse(success=True, data=get_real_portfolio()["rebalance"])
    except Exception as exc:
        return ApiResponse(success=True, message=f"fallback to demo: {exc}", data=get_demo_portfolio()["rebalance"])
