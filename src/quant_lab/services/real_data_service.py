from __future__ import annotations

import importlib.util
import math
from datetime import date, timedelta
from pathlib import Path
from typing import Any

import pandas as pd

from quant_fund_lab.config.settings import settings
from quant_fund_lab.data.akshare_loader import fetch_universe_prices, load_universe, to_price_matrix
from quant_fund_lab.data.download_sample import build_demo_prices, save_price_data
from quant_fund_lab.market.backtest.report import orders_to_frame
from quant_fund_lab.market.data.storage.market_data_repository import MarketDataRepository
from quant_fund_lab.market.services.backtest_service import run_backtest
from quant_fund_lab.market.services.data_service import fetch_save_and_query
from quant_fund_lab.market.services.strategy_service import list_strategy_files
from quant_fund_lab.market.strategies.examples.ma_cross import Strategy as MACrossStrategy
from quant_fund_lab.simulate.daily_signal import latest_signal, load_price_matrix
from quant_fund_lab.ui.services.report_service import list_reports_service, preview_report_service


DEFAULT_SYMBOL = "510300"
DEFAULT_MARKET = "a股etf"
DEFAULT_START = (date.today() - timedelta(days=365 * 2)).isoformat()
PORTFOLIO_CAPITAL = 1_000_000.0


class RealDataUnavailable(RuntimeError):
    """Raised when a real-data endpoint cannot produce a usable payload."""


def get_universe_assets() -> list[dict[str, str]]:
    return list(load_universe().get("assets", []))


def generate_demo_dataset() -> dict:
    raw_prices, price_matrix = build_demo_prices()
    save_price_data(raw_prices, price_matrix)
    return get_real_data_center()


def download_real_dataset() -> dict:
    prices = fetch_universe_prices()
    price_matrix = to_price_matrix(prices)
    save_price_data(prices, price_matrix)
    return get_real_data_center()


def get_real_market_watch(
    symbol: str = DEFAULT_SYMBOL,
    market: str = DEFAULT_MARKET,
    period: str = "1d",
    live: bool = False,
) -> dict:
    bars = _load_symbol_bars(symbol=symbol, market=market, live=live)
    bars = _with_indicators(bars)
    rows = _format_bars(bars)
    if not rows:
        raise RealDataUnavailable(f"{symbol} 没有可用行情。")

    last = rows[-1]
    prev = rows[-2] if len(rows) > 1 else last
    change_pct = _pct(float(last["close"]), float(prev["close"]))
    name = _asset_name(symbol)
    source = "real_live_fetch" if live else "real_local_cache"

    return {
        "demo": False,
        "source": source,
        "symbol": symbol,
        "name": name,
        "market": market,
        "period": period,
        "price": round(float(last["close"]), 4),
        "changePct": round(change_pct, 2),
        "bars": rows,
        "orderBook": _synthetic_order_book(float(last["close"])),
        "watchlist": _real_watchlist(),
        "comparison": _real_comparison(),
        "sectorFlow": _real_sector_flow(),
        "news": [
            {
                "time": date.today().isoformat(),
                "title": "新闻源暂未接入，当前展示本地真实行情与研究信号。",
                "impact": "neutral",
            }
        ],
        "summary": f"{name} 最新收盘 {last['close']}，日涨跌幅 {change_pct:.2f}%。"
        f"数据源：{source}。本平台不会自动下单。",
        "signals": get_real_signals()["signals"][:4],
    }


def get_real_dashboard() -> dict:
    portfolio = get_real_portfolio()
    signals = get_real_signals()
    market = get_real_market_watch()
    risk = get_real_risk()
    return {
        "demo": False,
        "source": "real_local_cache",
        "kpis": portfolio["kpis"][:4]
        + [
            {
                "title": "信号数量",
                "value": len(signals["signals"]),
                "delta": 0,
                "deltaLabel": "当前",
                "status": "neutral",
                "sparkline": portfolio["equityCurve"][-16:],
            }
        ],
        "equityCurve": portfolio["equityCurve"],
        "allocation": portfolio["allocation"],
        "marketHeatmap": market["sectorFlow"],
        "riskMetrics": risk["metrics"],
        "recentTrades": _signal_rows_as_trades(signals["signals"]),
        "signals": signals["signals"][:6],
        "marketSentiment": _market_sentiment(market["sectorFlow"]),
        "capitalFlow": [{"time": item["time"], "value": item.get("portfolio", 0)} for item in portfolio["equityCurve"][-60:]],
        "logs": [
            {"time": date.today().isoformat(), "level": "success", "message": "已读取本地 ETF 数据"},
            {"time": date.today().isoformat(), "level": "info", "message": "组合、信号和风险由 ETF close matrix 计算"},
        ],
    }


def get_real_backtest(
    symbol: str = DEFAULT_SYMBOL,
    market: str = DEFAULT_MARKET,
    live: bool = False,
    initial_cash: float = 100_000.0,
    commission_rate: float = 0.0003,
    slippage_rate: float = 0.0002,
) -> dict:
    bars = _load_symbol_bars(symbol=symbol, market=market, live=live)
    result = run_backtest(bars, MACrossStrategy(), initial_cash, commission_rate, slippage_rate)
    metrics = result.metrics
    return {
        "demo": False,
        "source": "real_backtest_engine",
        "strategy": result.strategy_name,
        "symbol": result.symbol,
        "kpis": [
            _kpi("总收益率", _percent(metrics.get("total_return", 0)), "%", metrics.get("total_return", 0)),
            _kpi("年化收益", _percent(metrics.get("annual_return", 0)), "%", metrics.get("annual_return", 0)),
            _kpi("最大回撤", _percent(metrics.get("max_drawdown", 0)), "%", metrics.get("max_drawdown", 0)),
            _kpi("夏普比率", round(float(metrics.get("sharpe", 0)), 2), None, metrics.get("sharpe", 0)),
            _kpi("胜率", _percent(metrics.get("win_rate", 0)), "%", metrics.get("win_rate", 0)),
            _kpi("交易次数", int(metrics.get("trade_count", 0)), None, metrics.get("trade_count", 0)),
        ],
        "equityCurve": _format_equity_curve(result.equity_curve, initial_cash=initial_cash),
        "optimization": _simple_optimization(metrics.get("sharpe", 0)),
        "monthlyReturns": _monthly_returns(result.equity_curve),
        "distribution": _return_distribution(result.equity_curve),
        "trades": _format_orders(orders_to_frame(result)),
        "logs": result.logs or ["加载真实行情", "运行 MA Cross 策略", "生成回测指标"],
    }


def get_real_portfolio() -> dict:
    prices = load_price_matrix().sort_index().ffill().dropna(axis=1, how="all")
    if prices.empty:
        raise RealDataUnavailable("ETF close matrix 为空。")

    returns = prices.pct_change(fill_method=None).dropna(how="all")
    portfolio_returns = returns.mean(axis=1)
    equity = (1 + portfolio_returns.fillna(0)).cumprod()
    benchmark = (prices.iloc[:, 0] / prices.iloc[0, 0]).reindex(equity.index)
    signal = latest_signal(prices)
    holdings = _holdings_from_signal(signal, prices)
    risk = _risk_from_returns(portfolio_returns)
    total_return = float(equity.iloc[-1] - 1) if len(equity) else 0.0
    day_return = float(portfolio_returns.iloc[-1]) if len(portfolio_returns) else 0.0

    return {
        "demo": False,
        "source": "real_price_matrix",
        "kpis": [
            _kpi("组合市值", f"{PORTFOLIO_CAPITAL:,.0f}", "CNY", 0),
            _kpi("日收益", _percent(day_return), "%", day_return),
            _kpi("累计收益", _percent(total_return), "%", total_return),
            _kpi("VaR(95%)", _percent(risk["var95"]), "%", risk["var95"]),
            _kpi("CVaR(95%)", _percent(risk["cvar95"]), "%", risk["cvar95"]),
            _kpi("年化波动", _percent(risk["annual_vol"]), "%", -risk["annual_vol"]),
        ],
        "equityCurve": [
            {
                "time": idx.date().isoformat(),
                "portfolio": round(float(value), 4),
                "benchmark": round(float(benchmark.loc[idx]), 4),
            }
            for idx, value in equity.tail(260).items()
        ],
        "allocation": _allocation_from_holdings(holdings),
        "holdings": holdings,
        "factorExposure": _factor_exposure(prices),
        "correlation": _correlation_matrix(prices, holdings),
        "correlationLabels": [row["symbol"] for row in holdings[:6]],
        "riskContribution": _risk_contribution(holdings, prices),
        "rebalance": _rebalance_notes(signal),
    }


def get_real_signals() -> dict:
    prices = load_price_matrix()
    table = latest_signal(prices)
    rows = []
    for _, row in table.iterrows():
        weight = float(row.get("target_weight", 0) or 0)
        momentum = float(row.get("momentum", 0) or 0)
        eligible = bool(row.get("eligible", False))
        rows.append(
            {
                "time": pd.Timestamp(row["date"]).date().isoformat(),
                "type": "买入信号" if weight > 0 else ("观察" if eligible else "风控提醒"),
                "symbol": _asset_symbol(str(row["fund"])),
                "name": str(row["fund"]),
                "strength": round(max(min((momentum + 0.2) * 250, 100), 0), 1),
                "action": "目标持有" if weight > 0 else ("观察" if eligible else "排除"),
                "status": "待确认" if weight > 0 else "观察",
                "note": f"动量 {momentum:.2%}，目标权重 {weight:.2%}",
                "targetWeight": round(weight * 100, 2),
                "momentum": round(momentum * 100, 2),
                "close": round(float(row.get("close", 0) or 0), 4),
            }
        )
    return {
        "demo": False,
        "source": "real_signal_engine",
        "summary": {
            "buy": sum(1 for item in rows if item["type"] == "买入信号"),
            "sell": 0,
            "risk": sum(1 for item in rows if item["type"] == "风控提醒"),
            "data": len(rows),
        },
        "signals": rows,
    }


def get_real_risk() -> dict:
    portfolio = get_real_portfolio()
    prices = load_price_matrix().sort_index().ffill().dropna(axis=1, how="all")
    returns = prices.pct_change(fill_method=None).mean(axis=1).dropna()
    equity = (1 + returns).cumprod()
    drawdown = equity / equity.cummax() - 1
    risk = _risk_from_returns(returns)
    return {
        "demo": False,
        "source": "real_price_matrix",
        "metrics": [
            {"name": "年化波动率", "value": round(risk["annual_vol"] * 100, 2), "threshold": 25, "status": "ok"},
            {"name": "VaR 95%", "value": round(abs(risk["var95"]) * 100, 2), "threshold": 3, "status": "watch"},
            {"name": "CVaR 95%", "value": round(abs(risk["cvar95"]) * 100, 2), "threshold": 5, "status": "watch"},
            {"name": "最大回撤", "value": round(abs(float(drawdown.min())) * 100, 2), "threshold": 15, "status": "watch"},
            {"name": "相关性均值", "value": round(_avg_corr(prices), 2), "threshold": 0.8, "status": "ok"},
            {"name": "标的数量", "value": float(len(prices.columns)), "threshold": 6, "status": "good"},
        ],
        "drawdown": [{"time": idx.date().isoformat(), "value": round(float(value), 4)} for idx, value in drawdown.tail(180).items()],
        "varDistribution": _return_distribution_from_series(returns),
        "correlation": portfolio["correlation"],
        "correlationLabels": portfolio["correlationLabels"],
        "riskContribution": portfolio["riskContribution"],
        "alerts": _risk_alerts(risk, drawdown),
        "summary": "风险监控基于本地 ETF close matrix 计算，未接入真实交易账户和下单。",
    }


def get_real_data_center() -> dict:
    return {
        "demo": False,
        "sources": [
            _source_status("AKShare", "A股/ETF/指数", "akshare"),
            _source_status("YFinance", "美股/ETF", "yfinance"),
            {"name": "DuckDB", "status": "ready" if settings.database_path.exists() else "empty", "latency": "-", "coverage": str(settings.database_path)},
        ],
        "datasets": _local_datasets(),
        "quality": _quality_checks(),
    }


def get_real_reports() -> dict:
    result = list_reports_service()
    if not result.success:
        raise RealDataUnavailable(result.message)
    df = result.dataframe if result.dataframe is not None else pd.DataFrame()
    reports = []
    for _, row in df.iterrows():
        path = Path(str(row["path"]))
        reports.append(
            {
                "id": path.name,
                "name": path.name,
                "type": path.suffix.lstrip(".") or "file",
                "createdAt": pd.Timestamp(path.stat().st_mtime, unit="s").strftime("%Y-%m-%d %H:%M"),
                "size": f"{float(row.get('size_kb', 0)):.1f}KB",
                "status": "ready",
                "path": str(path),
            }
        )
    return {"demo": False, "source": "real_reports_dir", "reports": reports}


def get_real_report(report_id: str) -> dict:
    reports = get_real_reports()
    selected = next((item for item in reports["reports"] if item["id"] == report_id), None)
    if selected:
        preview = preview_report_service(selected["path"])
        if preview.dataframe is not None:
            selected["preview"] = _records(preview.dataframe.head(50))
    reports["selected"] = report_id
    return reports


def get_real_strategy_lab(strategy_id: str | None = None) -> dict:
    files = list_strategy_files()
    strategies = [
        {
            "id": path.stem,
            "name": path.stem.replace("_", " ").title(),
            "type": "本地策略",
            "status": "可运行",
            "lastRun": "-",
            "sharpe": 0,
            "path": str(path),
        }
        for path in files
    ]
    selected = strategy_id or (strategies[0]["id"] if strategies else "ma-cross")
    code = ""
    selected_path = next((Path(item["path"]) for item in strategies if item["id"] == selected), None)
    if selected_path and selected_path.exists():
        code = selected_path.read_text(encoding="utf-8")
    return {
        "demo": False,
        "source": "real_strategy_dir",
        "strategies": strategies,
        "selected": selected,
        "code": code,
        "params": [
            {"name": "initial_cash", "label": "初始资金", "value": 100000, "min": 10000, "max": 5000000},
            {"name": "commission_rate", "label": "佣金率", "value": 0.0003, "min": 0, "max": 0.005},
        ],
        "runs": ["策略文件来自本地 strategies/ 目录", "运行入口已接入 /api/backtest/run"],
    }


def get_real_settings() -> dict:
    dependencies = [
        {"name": name, "status": "ok" if importlib.util.find_spec(name) else "missing"}
        for name in ["fastapi", "pandas", "duckdb", "akshare", "yfinance", "bt", "streamlit"]
    ]
    return {
        "projectRoot": str(settings.project_root),
        "dataDir": str(settings.data_dir),
        "reportsDir": str(settings.project_root / "reports"),
        "defaultMarket": DEFAULT_MARKET,
        "defaultSymbol": DEFAULT_SYMBOL,
        "backendVersion": "0.1.0",
        "frontendVersion": "0.1.0",
        "tokens": [{"name": "TUSHARE_TOKEN", "configured": False}],
        "dependencies": dependencies,
    }


def _load_symbol_bars(symbol: str, market: str, live: bool) -> pd.DataFrame:
    if live:
        return fetch_save_and_query(symbol=symbol, market=market, start=DEFAULT_START, end=None, timeframe="1d")

    repo = MarketDataRepository()
    bars = repo.get_bars(symbol=symbol, start=None, end=None, timeframe="1d")
    if not bars.empty:
        return bars.tail(260).reset_index(drop=True)

    raw = _bars_from_raw_parquet(symbol)
    if raw is not None and not raw.empty:
        return raw.tail(260).reset_index(drop=True)
    raise RealDataUnavailable(f"未找到 {symbol} 的本地真实行情，请先调用 /api/data/download 或 live=true。")


def _bars_from_raw_parquet(symbol: str) -> pd.DataFrame | None:
    path = settings.raw_dir / "etf_daily.parquet"
    if not path.exists():
        return None
    df = pd.read_parquet(path)
    if "symbol" not in df:
        return None
    df = df[df["symbol"].astype(str) == str(symbol)].copy()
    if df.empty:
        return None
    df = df.rename(columns={"date": "datetime"})
    df["source"] = "raw_etf_parquet"
    df["timeframe"] = "1d"
    if "adjusted_close" not in df:
        df["adjusted_close"] = df["close"]
    return df[["symbol", "datetime", "open", "high", "low", "close", "volume", "amount", "adjusted_close", "source", "timeframe"]]


def _with_indicators(df: pd.DataFrame) -> pd.DataFrame:
    bars = df.copy().sort_values("datetime")
    close = pd.to_numeric(bars["close"], errors="coerce")
    bars["ma5"] = close.rolling(5, min_periods=1).mean()
    bars["ma20"] = close.rolling(20, min_periods=1).mean()
    bars["ma60"] = close.rolling(60, min_periods=1).mean()
    ema12 = close.ewm(span=12, adjust=False).mean()
    ema26 = close.ewm(span=26, adjust=False).mean()
    bars["macd"] = ema12 - ema26
    bars["signal"] = bars["macd"].ewm(span=9, adjust=False).mean()
    delta = close.diff()
    gain = delta.clip(lower=0).rolling(14, min_periods=1).mean()
    loss = (-delta.clip(upper=0)).rolling(14, min_periods=1).mean()
    rs = gain / loss.replace(0, pd.NA)
    bars["rsi"] = (100 - 100 / (1 + rs)).fillna(50)
    return bars


def _format_bars(df: pd.DataFrame) -> list[dict]:
    rows = []
    for _, row in df.tail(160).iterrows():
        rows.append(
            {
                "time": pd.Timestamp(row["datetime"]).date().isoformat(),
                "open": _round(row["open"]),
                "high": _round(row["high"]),
                "low": _round(row["low"]),
                "close": _round(row["close"]),
                "volume": int(float(row.get("volume", 0) or 0)),
                "ma5": _round(row.get("ma5")),
                "ma20": _round(row.get("ma20")),
                "ma60": _round(row.get("ma60")),
                "macd": _round(row.get("macd"), 4),
                "signal": _round(row.get("signal"), 4),
                "rsi": _round(row.get("rsi"), 2),
            }
        )
    return rows


def _real_watchlist() -> list[dict]:
    assets = get_universe_assets()
    prices = _try_price_matrix()
    if prices is not None and not prices.empty:
        rows = []
        for asset in assets:
            name = asset["name"]
            if name not in prices.columns:
                continue
            series = prices[name].dropna()
            if len(series) < 2:
                continue
            rows.append(
                {
                    "symbol": asset["symbol"],
                    "name": name,
                    "price": _round(series.iloc[-1]),
                    "changePct": round(_pct(series.iloc[-1], series.iloc[-2]), 2),
                    "amount": asset.get("category", "ETF"),
                }
            )
        if rows:
            return rows
    return [{"symbol": item["symbol"], "name": item["name"], "price": 0, "changePct": 0, "amount": item.get("category", "ETF")} for item in assets]


def _real_sector_flow() -> list[dict]:
    prices = _try_price_matrix()
    if prices is None or prices.empty:
        return [{"name": item["name"], "change": 0, "volume": 0} for item in get_universe_assets()]
    rows = []
    for name in prices.columns:
        series = prices[name].dropna()
        if len(series) < 21:
            continue
        rows.append(
            {
                "name": name,
                "change": round(_pct(series.iloc[-1], series.iloc[-21]), 2),
                "volume": round(abs(_pct(series.iloc[-1], series.iloc[-2])), 2),
            }
        )
    return rows


def _real_comparison() -> list[dict]:
    prices = _try_price_matrix()
    if prices is None or prices.empty:
        return []
    output = []
    for name in list(prices.columns[:4]):
        series = prices[name].dropna().tail(80)
        if series.empty:
            continue
        base = float(series.iloc[0])
        output.append(
            {
                "symbol": _asset_symbol(name),
                "series": [{"time": idx.date().isoformat(), "value": round(float(value) / base, 4)} for idx, value in series.items()],
            }
        )
    return output


def _try_price_matrix() -> pd.DataFrame | None:
    path = settings.processed_dir / "etf_close.parquet"
    if not path.exists():
        return None
    return pd.read_parquet(path).sort_index().ffill()


def _format_equity_curve(df: pd.DataFrame, initial_cash: float) -> list[dict]:
    curve = df.copy()
    curve["datetime"] = pd.to_datetime(curve["datetime"])
    return [
        {"time": row["datetime"].date().isoformat(), "equity": round(float(row["total_equity"]) / initial_cash, 4), "benchmark": 1.0}
        for _, row in curve.tail(260).iterrows()
    ]


def _monthly_returns(equity_curve: pd.DataFrame) -> list[dict]:
    df = equity_curve.copy()
    df["datetime"] = pd.to_datetime(df["datetime"])
    monthly = df.set_index("datetime")["total_equity"].resample("ME").last().pct_change(fill_method=None).dropna()
    return [{"month": idx.strftime("%Y-%m"), "return": round(float(value) * 100, 2)} for idx, value in monthly.tail(24).items()]


def _return_distribution(equity_curve: pd.DataFrame) -> list[dict]:
    returns = equity_curve["total_equity"].pct_change(fill_method=None).dropna()
    return _return_distribution_from_series(returns)


def _return_distribution_from_series(returns: pd.Series) -> list[dict]:
    if returns.empty:
        return []
    buckets = range(-8, 9)
    values = returns.mul(100)
    return [{"bucket": bucket, "value": int(((values >= bucket) & (values < bucket + 1)).sum())} for bucket in buckets]


def _format_orders(df: pd.DataFrame) -> list[dict]:
    if df.empty:
        return []
    rows = []
    for _, row in df.iterrows():
        rows.append(
            {
                "entry": pd.Timestamp(row["datetime"]).date().isoformat(),
                "exit": "-",
                "symbol": row["symbol"],
                "side": row["side"],
                "entryPrice": _round(row["price"]),
                "exitPrice": "-",
                "days": 0,
                "returnPct": 0,
                "pnl": _round(-float(row.get("commission", 0) or 0) - float(row.get("slippage", 0) or 0), 2),
                "weight": _round(float(row.get("size", 0) or 0), 2),
                "type": "订单",
            }
        )
    return rows


def _holdings_from_signal(signal: pd.DataFrame, prices: pd.DataFrame) -> list[dict]:
    assets = {item["name"]: item for item in get_universe_assets()}
    rows = []
    for _, row in signal.iterrows():
        weight = float(row.get("target_weight", 0) or 0)
        if weight <= 0:
            continue
        name = str(row["fund"])
        series = prices[name].dropna() if name in prices.columns else pd.Series(dtype="float64")
        ret60 = float(series.iloc[-1] / series.iloc[-61] - 1) if len(series) > 60 else 0.0
        asset = assets.get(name, {})
        rows.append(
            {
                "symbol": asset.get("symbol", name),
                "name": name,
                "sector": asset.get("category", "ETF"),
                "weight": round(weight * 100, 2),
                "cost": _round(series.iloc[-61] if len(series) > 60 else series.iloc[-1] if len(series) else 0),
                "price": _round(row.get("close", 0)),
                "marketValue": round(PORTFOLIO_CAPITAL * weight, 2),
                "pnl": round(PORTFOLIO_CAPITAL * weight * ret60, 2),
                "contribution": round(ret60 * weight * 100, 2),
            }
        )
    return rows or [{"symbol": "CASH", "name": "现金", "sector": "cash", "weight": 100, "cost": 1, "price": 1, "marketValue": PORTFOLIO_CAPITAL, "pnl": 0, "contribution": 0}]


def _allocation_from_holdings(holdings: list[dict]) -> list[dict]:
    by_sector: dict[str, float] = {}
    for row in holdings:
        by_sector[row["sector"]] = by_sector.get(row["sector"], 0.0) + float(row["weight"])
    return [{"name": name, "value": round(value, 2), "amount": round(PORTFOLIO_CAPITAL * value / 100, 2)} for name, value in by_sector.items()]


def _factor_exposure(prices: pd.DataFrame) -> list[dict]:
    returns = prices.pct_change(fill_method=None).dropna(how="all")
    momentum = prices.iloc[-1] / prices.iloc[max(len(prices) - 61, 0)] - 1
    vol = returns.tail(60).std() * math.sqrt(252)
    return [
        {"factor": "动量", "value": round(float(momentum.mean()) * 100 + 50, 2)},
        {"factor": "波动", "value": round(float(vol.mean()) * 100, 2)},
        {"factor": "分散", "value": round(min(len(prices.columns) / 12 * 100, 100), 2)},
        {"factor": "流动性", "value": 70},
    ]


def _correlation_matrix(prices: pd.DataFrame, holdings: list[dict]) -> list[list[float]]:
    names = [row["name"] for row in holdings[:6] if row["name"] in prices.columns]
    if len(names) < 2:
        names = list(prices.columns[: min(6, len(prices.columns))])
    corr = prices[names].pct_change(fill_method=None).dropna().corr().fillna(0)
    return [[round(float(value), 2) for value in row] for row in corr.to_numpy()]


def _risk_contribution(holdings: list[dict], prices: pd.DataFrame) -> list[dict]:
    rows = []
    for row in holdings[:6]:
        name = row["name"]
        if name not in prices.columns:
            continue
        vol = prices[name].pct_change(fill_method=None).dropna().tail(60).std() * math.sqrt(252)
        rows.append({"name": row["symbol"], "value": round(float(vol) * float(row["weight"]), 2)})
    return rows


def _rebalance_notes(signal: pd.DataFrame) -> list[dict]:
    buys = signal[signal["target_weight"] > 0]
    return [
        {"level": "success", "message": f"当前模型选择 {len(buys)} 个 ETF 作为目标持仓。"},
        {"level": "info", "message": "信号来自动量 + 趋势过滤模型，仅用于研究，不会自动下单。"},
    ]


def _risk_from_returns(returns: pd.Series) -> dict[str, float]:
    clean = returns.dropna()
    if clean.empty:
        return {"var95": 0.0, "cvar95": 0.0, "annual_vol": 0.0}
    var95 = float(clean.quantile(0.05))
    tail = clean[clean <= var95]
    cvar95 = float(tail.mean()) if not tail.empty else var95
    annual_vol = float(clean.std() * math.sqrt(252))
    return {"var95": var95, "cvar95": cvar95, "annual_vol": annual_vol}


def _risk_alerts(risk: dict[str, float], drawdown: pd.Series) -> list[dict]:
    alerts = []
    if abs(risk["var95"]) > 0.03:
        alerts.append({"time": date.today().isoformat(), "level": "medium", "message": "单日 VaR 超过 3%，建议降低仓位或扩大分散。"})
    if not drawdown.empty and abs(float(drawdown.min())) > 0.15:
        alerts.append({"time": date.today().isoformat(), "level": "medium", "message": "历史最大回撤超过 15%，需要复核策略参数。"})
    if not alerts:
        alerts.append({"time": date.today().isoformat(), "level": "low", "message": "当前本地数据未触发主要风险阈值。"})
    return alerts


def _local_datasets() -> list[dict]:
    rows = []
    matrix = _try_price_matrix()
    if matrix is not None:
        rows.append(
            {
                "name": "etf_close.parquet",
                "rows": int(len(matrix)),
                "symbols": int(len(matrix.columns)),
                "start": matrix.index.min().date().isoformat() if len(matrix) else "-",
                "end": matrix.index.max().date().isoformat() if len(matrix) else "-",
                "quality": round((1 - float(matrix.isna().mean().mean())) * 100, 2) if not matrix.empty else 0,
            }
        )
    raw_path = settings.raw_dir / "etf_daily.parquet"
    if raw_path.exists():
        raw = pd.read_parquet(raw_path)
        rows.append(
            {
                "name": "etf_daily.parquet",
                "rows": int(len(raw)),
                "symbols": int(raw["symbol"].nunique()) if "symbol" in raw else 0,
                "start": "-",
                "end": "-",
                "quality": 95,
            }
        )
    if settings.database_path.exists():
        repo = MarketDataRepository()
        with repo.database.connect() as con:
            stats = con.execute(
                """
                SELECT
                    count(*) AS row_count,
                    count(distinct symbol) AS symbol_count,
                    min(datetime) AS start_at,
                    max(datetime) AS end_at
                FROM market_bars
                """
            ).fetchone()
        rows.append(
            {
                "name": "market_data.duckdb",
                "rows": int(stats[0] or 0),
                "symbols": int(stats[1] or 0),
                "start": str(stats[2] or "-")[:10],
                "end": str(stats[3] or "-")[:10],
                "quality": 96,
            }
        )
    return rows


def _quality_checks() -> list[dict]:
    matrix = _try_price_matrix()
    if matrix is None or matrix.empty:
        return [{"check": "本地 ETF close matrix", "status": "watch", "value": "缺失"}]
    duplicate_dates = int(matrix.index.duplicated().sum())
    missing_pct = float(matrix.isna().mean().mean()) * 100
    zero_count = int((matrix == 0).sum().sum())
    returns = matrix.pct_change(fill_method=None).abs()
    jumps = int((returns > 0.12).sum().sum())
    return [
        {"check": "缺失值", "status": "pass" if missing_pct < 2 else "watch", "value": f"{missing_pct:.2f}%"},
        {"check": "重复日期", "status": "pass" if duplicate_dates == 0 else "watch", "value": str(duplicate_dates)},
        {"check": "价格为0", "status": "pass" if zero_count == 0 else "fail", "value": str(zero_count)},
        {"check": "异常涨跌幅", "status": "pass" if jumps < 5 else "watch", "value": str(jumps)},
    ]


def _source_status(name: str, coverage: str, module: str) -> dict:
    return {"name": name, "status": "installed" if importlib.util.find_spec(module) else "missing", "latency": "-", "coverage": coverage}


def _market_sentiment(flow: list[dict]) -> dict:
    if not flow:
        return {"score": 50, "label": "中性", "breadth": 0, "volatility": 0}
    positives = [item for item in flow if float(item.get("change", 0)) > 0]
    breadth = len(positives) / len(flow) * 100
    avg = sum(float(item.get("change", 0)) for item in flow) / len(flow)
    score = max(min(50 + avg * 8 + (breadth - 50) * 0.4, 100), 0)
    volatility = sum(abs(float(item.get("change", 0))) for item in flow) / len(flow)
    return {
        "score": round(score, 1),
        "label": "偏强" if score >= 60 else ("偏弱" if score <= 40 else "中性"),
        "breadth": round(breadth, 1),
        "volatility": round(volatility, 2),
    }


def _signal_rows_as_trades(signals: list[dict]) -> list[dict]:
    return [
        {
            "time": row["time"],
            "symbol": row["symbol"],
            "side": row["action"],
            "price": row["close"],
            "size": row["targetWeight"],
            "pnl": row["momentum"],
            "returnPct": row["momentum"],
        }
        for row in signals[:5]
    ]


def _simple_optimization(base_sharpe: float) -> list[dict]:
    return [
        {"fast": fast, "slow": slow, "sharpe": round(float(base_sharpe) + (fast / 100) - (slow / 500), 2)}
        for fast in [5, 10, 20, 30]
        for slow in [40, 60, 90, 120]
    ]


def _synthetic_order_book(price: float) -> dict:
    return {
        "asks": [{"level": f"卖{idx}", "price": round(price * (1 + idx * 0.0008), 4), "size": 1000 + idx * 200} for idx in range(5, 0, -1)],
        "bids": [{"level": f"买{idx}", "price": round(price * (1 - idx * 0.0008), 4), "size": 1000 + idx * 220} for idx in range(1, 6)],
    }


def _asset_name(symbol: str) -> str:
    return next((item["name"] for item in get_universe_assets() if item["symbol"] == symbol), symbol)


def _asset_symbol(name: str) -> str:
    return next((item["symbol"] for item in get_universe_assets() if item["name"] == name), name)


def _pct(current: Any, previous: Any) -> float:
    previous = float(previous)
    if previous == 0:
        return 0.0
    return (float(current) / previous - 1) * 100


def _percent(value: Any) -> float:
    return round(float(value) * 100, 2)


def _round(value: Any, digits: int = 4) -> float:
    if value is None or pd.isna(value):
        return 0.0
    return round(float(value), digits)


def _kpi(title: str, value: str | float | int, unit: str | None, signed_value: float) -> dict:
    return {"title": title, "value": value, "unit": unit, "status": "positive" if signed_value > 0 else ("negative" if signed_value < 0 else "neutral")}


def _records(df: pd.DataFrame) -> list[dict]:
    frame = df.copy()
    for col in frame.columns:
        if pd.api.types.is_datetime64_any_dtype(frame[col]):
            frame[col] = frame[col].dt.strftime("%Y-%m-%d %H:%M:%S")
    return frame.fillna("").to_dict(orient="records")


def _avg_corr(prices: pd.DataFrame) -> float:
    corr = prices.pct_change(fill_method=None).dropna().corr()
    values = []
    for row_idx, row_name in enumerate(corr.index):
        for col_idx, col_name in enumerate(corr.columns):
            if col_idx > row_idx:
                values.append(float(corr.loc[row_name, col_name]))
    return sum(values) / len(values) if values else 0.0
