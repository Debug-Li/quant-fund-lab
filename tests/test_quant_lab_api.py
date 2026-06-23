from __future__ import annotations

from fastapi.testclient import TestClient

from quant_lab.api.main import app
from quant_lab.services.demo_data_service import (
    get_demo_backtest,
    get_demo_dashboard,
    get_demo_market_watch,
    get_demo_portfolio,
    get_demo_risk,
)


client = TestClient(app)


def test_health_api() -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["success"] is True


def test_dashboard_api_returns_complete_demo_payload() -> None:
    response = client.get("/api/dashboard/overview")
    payload = response.json()
    assert payload["success"] is True
    assert {"kpis", "equityCurve", "allocation", "marketHeatmap", "signals"}.issubset(payload["data"])


def test_core_page_apis_return_demo_data() -> None:
    endpoints = [
        "/api/market/snapshot?symbol=NVDA",
        "/api/portfolio/overview",
        "/api/risk/overview",
        "/api/signal/list",
        "/api/data/status",
        "/api/report/list",
        "/api/settings",
        "/api/strategy/ma-cross",
    ]
    for endpoint in endpoints:
        response = client.get(endpoint)
        assert response.status_code == 200
        assert response.json()["success"] is True


def test_backtest_run_api() -> None:
    response = client.post("/api/backtest/run")
    payload = response.json()
    assert response.status_code == 200
    assert payload["success"] is True
    assert payload["data"]["kpis"]


def test_demo_data_services_are_non_empty() -> None:
    assert get_demo_dashboard()["equityCurve"]
    assert get_demo_market_watch("NVDA")["bars"]
    assert get_demo_backtest()["trades"]
    assert get_demo_portfolio()["holdings"]
    assert get_demo_risk()["alerts"]
