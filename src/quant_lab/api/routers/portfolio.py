from __future__ import annotations

from fastapi import APIRouter

from quant_lab.schemas.response import ApiResponse
from quant_lab.services.demo_data_service import get_demo_portfolio


router = APIRouter()


@router.get("/overview", response_model=ApiResponse)
def overview() -> ApiResponse:
    return ApiResponse(success=True, data=get_demo_portfolio())


@router.get("/holdings", response_model=ApiResponse)
def holdings() -> ApiResponse:
    return ApiResponse(success=True, data=get_demo_portfolio()["holdings"])


@router.get("/risk", response_model=ApiResponse)
def risk() -> ApiResponse:
    data = get_demo_portfolio()
    return ApiResponse(success=True, data={"factorExposure": data["factorExposure"], "correlation": data["correlation"], "riskContribution": data["riskContribution"]})


@router.get("/rebalance/suggestion", response_model=ApiResponse)
def rebalance_suggestion() -> ApiResponse:
    return ApiResponse(success=True, data=get_demo_portfolio()["rebalance"])
