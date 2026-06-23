from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from quant_lab.api.routers import backtest, dashboard, data, market, portfolio, report, risk, settings, signal, strategy
from quant_lab.schemas.response import ApiResponse


def create_app() -> FastAPI:
    app = FastAPI(title="量观 Quant Lab API", version="0.1.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])
    app.include_router(market.router, prefix="/api/market", tags=["market"])
    app.include_router(strategy.router, prefix="/api/strategy", tags=["strategy"])
    app.include_router(backtest.router, prefix="/api/backtest", tags=["backtest"])
    app.include_router(portfolio.router, prefix="/api/portfolio", tags=["portfolio"])
    app.include_router(signal.router, prefix="/api/signal", tags=["signal"])
    app.include_router(data.router, prefix="/api/data", tags=["data"])
    app.include_router(risk.router, prefix="/api/risk", tags=["risk"])
    app.include_router(report.router, prefix="/api/report", tags=["report"])
    app.include_router(settings.router, prefix="/api/settings", tags=["settings"])
    return app


app = create_app()


@app.get("/api/health", response_model=ApiResponse)
def health() -> ApiResponse:
    return ApiResponse(success=True, message="ok", data={"status": "ok", "product": "量观 Quant Lab"})
