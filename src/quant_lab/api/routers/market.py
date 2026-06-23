from __future__ import annotations

from fastapi import APIRouter

from quant_lab.schemas.response import ApiResponse
from quant_lab.services.demo_data_service import get_demo_market_watch


router = APIRouter()


@router.get("/snapshot", response_model=ApiResponse)
def snapshot(symbol: str = "NVDA", market: str = "US", period: str = "1d") -> ApiResponse:
    data = get_demo_market_watch(symbol)
    data["market"] = market
    data["period"] = period
    return ApiResponse(success=True, message="demo market snapshot", data=data)


@router.get("/watchlist", response_model=ApiResponse)
def watchlist() -> ApiResponse:
    return ApiResponse(success=True, data=get_demo_market_watch()["watchlist"])


@router.get("/sector-flow", response_model=ApiResponse)
def sector_flow() -> ApiResponse:
    return ApiResponse(success=True, data=get_demo_market_watch()["sectorFlow"])


@router.get("/news", response_model=ApiResponse)
def news() -> ApiResponse:
    return ApiResponse(success=True, data=get_demo_market_watch()["news"])
