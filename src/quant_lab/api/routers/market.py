from __future__ import annotations

from fastapi import APIRouter

from quant_lab.schemas.response import ApiResponse
from quant_lab.services.demo_data_service import get_demo_market_watch
from quant_lab.services.real_data_service import DEFAULT_MARKET, DEFAULT_SYMBOL, get_real_market_watch


router = APIRouter()


@router.get("/snapshot", response_model=ApiResponse)
def snapshot(symbol: str = DEFAULT_SYMBOL, market: str = DEFAULT_MARKET, period: str = "1d", live: bool = False) -> ApiResponse:
    try:
        return ApiResponse(success=True, message="real market snapshot", data=get_real_market_watch(symbol, market, period, live))
    except Exception as exc:
        data = get_demo_market_watch(symbol)
        data["market"] = market
        data["period"] = period
        data["fallbackReason"] = str(exc)
        return ApiResponse(success=True, message="real market unavailable, fallback to demo", data=data)


@router.get("/watchlist", response_model=ApiResponse)
def watchlist() -> ApiResponse:
    try:
        return ApiResponse(success=True, data=get_real_market_watch()["watchlist"])
    except Exception as exc:
        return ApiResponse(success=True, message=f"fallback to demo: {exc}", data=get_demo_market_watch()["watchlist"])


@router.get("/sector-flow", response_model=ApiResponse)
def sector_flow() -> ApiResponse:
    try:
        return ApiResponse(success=True, data=get_real_market_watch()["sectorFlow"])
    except Exception as exc:
        return ApiResponse(success=True, message=f"fallback to demo: {exc}", data=get_demo_market_watch()["sectorFlow"])


@router.get("/news", response_model=ApiResponse)
def news() -> ApiResponse:
    try:
        return ApiResponse(success=True, data=get_real_market_watch()["news"])
    except Exception as exc:
        return ApiResponse(success=True, message=f"fallback to demo: {exc}", data=get_demo_market_watch()["news"])
