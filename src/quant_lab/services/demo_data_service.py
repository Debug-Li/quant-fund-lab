from __future__ import annotations

import math
from datetime import date, timedelta
from random import Random


RNG = Random(42)


def _dates(days: int = 160) -> list[str]:
    today = date(2026, 6, 23)
    return [(today - timedelta(days=days - idx)).isoformat() for idx in range(days)]


def _series(days: int, start: float, drift: float = 0.001, wave: float = 0.025) -> list[dict]:
    values = []
    value = start
    for idx, day in enumerate(_dates(days)):
        value *= 1 + drift + math.sin(idx / 8) * wave / 10 + RNG.uniform(-0.006, 0.006)
        values.append({"time": day, "value": round(value, 4)})
    return values


def _ohlcv(symbol: str = "NVDA", days: int = 120) -> list[dict]:
    rows = []
    base = 780.0 if symbol == "NVDA" else 520.0
    for idx, day in enumerate(_dates(days)):
        close = base * (1 + idx * 0.0025 + math.sin(idx / 7) * 0.035 + RNG.uniform(-0.012, 0.012))
        open_ = close * (1 + RNG.uniform(-0.008, 0.008))
        high = max(open_, close) * (1 + RNG.uniform(0.002, 0.018))
        low = min(open_, close) * (1 - RNG.uniform(0.002, 0.018))
        rows.append(
            {
                "time": day,
                "open": round(open_, 2),
                "high": round(high, 2),
                "low": round(low, 2),
                "close": round(close, 2),
                "volume": int(28_000_000 + RNG.random() * 50_000_000),
                "ma5": round(close * (1 + math.sin(idx / 12) * 0.01), 2),
                "ma20": round(close * (1 - math.cos(idx / 18) * 0.014), 2),
                "ma60": round(close * 0.96, 2),
                "macd": round(math.sin(idx / 9) * 2.6, 3),
                "signal": round(math.sin(idx / 11) * 2.1, 3),
                "rsi": round(48 + math.sin(idx / 10) * 22, 2),
            }
        )
    return rows


def _heatmap() -> list[dict]:
    names = ["科技", "半导体", "软件", "金融", "医疗", "消费电子", "工业", "通信", "能源", "材料", "公用事业", "房地产"]
    return [
        {"name": name, "change": round(RNG.uniform(-2.8, 3.6), 2), "volume": round(RNG.uniform(18, 120), 1)}
        for name in names
    ]


def _signals() -> list[dict]:
    return [
        {"time": "09:35", "type": "买入信号", "symbol": "NVDA", "name": "英伟达", "strength": 92, "action": "加仓", "status": "待确认", "note": "突破20日新高"},
        {"time": "10:12", "type": "风控提醒", "symbol": "TSLA", "name": "特斯拉", "strength": 66, "action": "降权", "status": "观察", "note": "波动率升高"},
        {"time": "13:48", "type": "数据更新", "symbol": "SPY", "name": "标普500ETF", "strength": 50, "action": "刷新", "status": "已完成", "note": "行情缓存更新"},
        {"time": "14:22", "type": "卖出信号", "symbol": "XLE", "name": "能源ETF", "strength": 73, "action": "减仓", "status": "待确认", "note": "动量转弱"},
    ]


def get_demo_dashboard() -> dict:
    equity = _series(180, 1.0, 0.0018)
    benchmark = _series(180, 1.0, 0.0011)
    return {
        "demo": True,
        "kpis": [
            {"title": "总资产", "value": "1,286,420", "unit": "CNY", "delta": 1.82, "deltaLabel": "今日", "status": "positive", "sparkline": _series(16, 100)},
            {"title": "今日收益", "value": "23,480", "unit": "CNY", "delta": 1.86, "deltaLabel": "较昨日", "status": "positive", "sparkline": _series(16, 100, 0.002)},
            {"title": "累计收益率", "value": "38.7", "unit": "%", "delta": 4.2, "deltaLabel": "近30日", "status": "positive", "sparkline": _series(16, 100, 0.003)},
            {"title": "最大回撤", "value": "-8.4", "unit": "%", "delta": -0.6, "deltaLabel": "风险", "status": "negative", "sparkline": _series(16, 100, -0.001)},
            {"title": "夏普比率", "value": "1.76", "delta": 0.11, "deltaLabel": "滚动", "status": "neutral", "sparkline": _series(16, 100, 0.001)},
        ],
        "equityCurve": [{"time": p["time"], "portfolio": p["value"], "benchmark": benchmark[idx]["value"]} for idx, p in enumerate(equity)],
        "allocation": [
            {"name": "股票", "value": 42, "amount": 540296},
            {"name": "ETF", "value": 31, "amount": 398790},
            {"name": "现金", "value": 12, "amount": 154370},
            {"name": "期货", "value": 9, "amount": 115778},
            {"name": "其他", "value": 6, "amount": 77185},
        ],
        "marketHeatmap": _heatmap(),
        "riskMetrics": [
            {"name": "年化波动率", "value": 18.6, "threshold": 25, "status": "ok"},
            {"name": "Beta", "value": 1.08, "threshold": 1.2, "status": "ok"},
            {"name": "Alpha", "value": 6.2, "threshold": 0, "status": "good"},
            {"name": "最大回撤", "value": 8.4, "threshold": 12, "status": "watch"},
            {"name": "胜率", "value": 61.5, "threshold": 50, "status": "good"},
            {"name": "换手率", "value": 28.0, "threshold": 45, "status": "ok"},
        ],
        "recentTrades": [
            {"time": "14:31", "symbol": "NVDA", "side": "BUY", "price": 842.3, "size": 120, "pnl": 4280, "returnPct": 3.8},
            {"time": "13:52", "symbol": "510300", "side": "SELL", "price": 3.72, "size": 50000, "pnl": 1850, "returnPct": 1.1},
            {"time": "11:18", "symbol": "QQQ", "side": "BUY", "price": 529.4, "size": 80, "pnl": -420, "returnPct": -0.6},
        ],
        "signals": _signals(),
        "marketSentiment": {"score": 72, "label": "偏强", "breadth": 64, "volatility": 18.2},
        "capitalFlow": _series(60, 40, 0.006),
        "logs": [
            {"time": "09:00", "level": "info", "message": "加载本地缓存行情"},
            {"time": "09:32", "level": "success", "message": "策略信号生成完成"},
            {"time": "15:05", "level": "warning", "message": "能源板块动量转弱"},
        ],
    }


def get_demo_market_watch(symbol: str = "NVDA") -> dict:
    bars = _ohlcv(symbol)
    last = bars[-1]
    return {
        "demo": True,
        "symbol": symbol,
        "name": "英伟达" if symbol == "NVDA" else symbol,
        "price": last["close"],
        "changePct": 2.34,
        "bars": bars,
        "orderBook": {
            "asks": [{"level": f"卖{idx}", "price": round(last["close"] + idx * 0.28, 2), "size": 1400 + idx * 260} for idx in range(5, 0, -1)],
            "bids": [{"level": f"买{idx}", "price": round(last["close"] - idx * 0.26, 2), "size": 1800 + idx * 310} for idx in range(1, 6)],
        },
        "watchlist": [
            {"symbol": "NVDA", "name": "英伟达", "price": 842.3, "changePct": 2.34, "amount": "128.4B"},
            {"symbol": "AAPL", "name": "苹果", "price": 214.6, "changePct": -0.42, "amount": "84.1B"},
            {"symbol": "SPY", "name": "标普500ETF", "price": 744.4, "changePct": 0.68, "amount": "62.9B"},
            {"symbol": "510300", "name": "沪深300ETF", "price": 3.72, "changePct": 1.12, "amount": "22.7B"},
        ],
        "comparison": [
            {"symbol": "NVDA", "series": _series(80, 100, 0.0025)},
            {"symbol": "AAPL", "series": _series(80, 100, 0.0012)},
            {"symbol": "SPY", "series": _series(80, 100, 0.0010)},
            {"symbol": "QQQ", "series": _series(80, 100, 0.0016)},
        ],
        "sectorFlow": _heatmap(),
        "news": [
            {"time": "09:18", "title": "半导体板块资金流入居前", "impact": "positive"},
            {"time": "10:45", "title": "美债收益率回落提升风险偏好", "impact": "neutral"},
            {"time": "13:30", "title": "AI 服务器链订单维持高景气", "impact": "positive"},
        ],
        "summary": "今日科技与半导体板块动能较强，NVDA 保持多头趋势。短线需关注大盘波动和高位成交量变化。",
        "signals": _signals(),
    }


def get_demo_backtest() -> dict:
    equity = _series(220, 1.0, 0.0017)
    return {
        "demo": True,
        "strategy": "MA 动量轮动",
        "kpis": [
            {"title": "总收益率", "value": "42.6", "unit": "%", "status": "positive"},
            {"title": "年化收益", "value": "18.9", "unit": "%", "status": "positive"},
            {"title": "最大回撤", "value": "-9.8", "unit": "%", "status": "negative"},
            {"title": "夏普比率", "value": "1.64", "status": "neutral"},
            {"title": "胜率", "value": "62.0", "unit": "%", "status": "positive"},
            {"title": "Calmar", "value": "1.93", "status": "neutral"},
        ],
        "equityCurve": [{"time": p["time"], "equity": p["value"], "benchmark": round(1 + idx * 0.0011, 4)} for idx, p in enumerate(equity)],
        "optimization": [{"fast": f, "slow": s, "sharpe": round(0.7 + f / 80 + s / 260 + RNG.random() * 0.4, 2)} for f in [5, 10, 20, 30] for s in [40, 60, 90, 120]],
        "monthlyReturns": [{"month": f"2026-{m:02d}", "return": round(RNG.uniform(-4.2, 6.4), 2)} for m in range(1, 13)],
        "distribution": [{"bucket": x, "value": round(math.exp(-(x / 3) ** 2) * 100 + RNG.random() * 8, 2)} for x in range(-8, 9)],
        "trades": [
            {"entry": "2026-01-08", "exit": "2026-02-14", "symbol": "510300", "side": "LONG", "entryPrice": 3.42, "exitPrice": 3.68, "days": 37, "returnPct": 7.6, "pnl": 12800, "weight": 0.25, "type": "轮动"},
            {"entry": "2026-03-02", "exit": "2026-04-18", "symbol": "NVDA", "side": "LONG", "entryPrice": 728.1, "exitPrice": 815.6, "days": 47, "returnPct": 12.0, "pnl": 21300, "weight": 0.18, "type": "突破"},
            {"entry": "2026-05-06", "exit": "2026-05-29", "symbol": "XLE", "side": "LONG", "entryPrice": 88.2, "exitPrice": 85.4, "days": 23, "returnPct": -3.2, "pnl": -3100, "weight": 0.10, "type": "止损"},
        ],
        "logs": [
            "开始初始化回测环境",
            "加载标的池数据",
            "生成策略信号",
            "执行交易撮合",
            "计算权益曲线",
            "回测完成",
        ],
    }


def get_demo_portfolio() -> dict:
    return {
        "demo": True,
        "kpis": [
            {"title": "组合市值", "value": "1,286,420", "unit": "CNY", "status": "neutral"},
            {"title": "日收益", "value": "1.82", "unit": "%", "status": "positive"},
            {"title": "累计收益", "value": "38.7", "unit": "%", "status": "positive"},
            {"title": "VaR(95%)", "value": "-2.8", "unit": "%", "status": "negative"},
            {"title": "CVaR(95%)", "value": "-4.1", "unit": "%", "status": "negative"},
            {"title": "杠杆率", "value": "1.05", "status": "neutral"},
        ],
        "equityCurve": get_demo_dashboard()["equityCurve"],
        "allocation": get_demo_dashboard()["allocation"],
        "holdings": [
            {"symbol": "NVDA", "name": "英伟达", "sector": "半导体", "weight": 14.2, "cost": 728.1, "price": 842.3, "marketValue": 212860, "pnl": 28800, "contribution": 2.24},
            {"symbol": "510300", "name": "沪深300ETF", "sector": "宽基ETF", "weight": 13.1, "cost": 3.38, "price": 3.72, "marketValue": 168520, "pnl": 15420, "contribution": 1.20},
            {"symbol": "QQQ", "name": "纳指100ETF", "sector": "科技ETF", "weight": 11.8, "cost": 501.3, "price": 529.4, "marketValue": 151820, "pnl": 8100, "contribution": 0.63},
        ],
        "factorExposure": [{"factor": name, "value": value} for name, value in [("动量", 82), ("质量", 68), ("价值", 42), ("波动", 55), ("成长", 76), ("流动性", 64)]],
        "correlation": [[1, 0.62, 0.71], [0.62, 1, 0.48], [0.71, 0.48, 1]],
        "correlationLabels": ["NVDA", "510300", "QQQ"],
        "riskContribution": [{"name": "NVDA", "value": 32}, {"name": "510300", "value": 18}, {"name": "QQQ", "value": 24}, {"name": "现金", "value": 4}],
        "rebalance": [
            {"level": "warning", "message": "半导体权重接近阈值，建议保留观察"},
            {"level": "info", "message": "现金占比 12%，流动性充足"},
            {"level": "success", "message": "组合相关性均值 0.60，分散度良好"},
        ],
    }


def get_demo_signals() -> dict:
    return {"demo": True, "summary": {"buy": 4, "sell": 2, "risk": 3, "data": 1}, "signals": _signals()}


def get_demo_risk() -> dict:
    return {
        "demo": True,
        "metrics": get_demo_portfolio()["kpis"],
        "drawdown": [{"time": p["time"], "value": round(min(0, math.sin(idx / 10) * -0.08), 4)} for idx, p in enumerate(_series(140, 1.0))],
        "varDistribution": [{"bucket": x, "value": round(math.exp(-(x / 2.5) ** 2) * 100, 2)} for x in range(-8, 9)],
        "correlation": get_demo_portfolio()["correlation"],
        "correlationLabels": get_demo_portfolio()["correlationLabels"],
        "riskContribution": get_demo_portfolio()["riskContribution"],
        "alerts": [
            {"time": "10:12", "level": "medium", "message": "TSLA 波动率超过阈值"},
            {"time": "14:40", "level": "low", "message": "现金占比充足，无流动性风险"},
        ],
        "summary": "当前组合处于中低风险区间，主要风险来自半导体仓位和科技板块相关性。",
    }


def get_demo_reports() -> dict:
    return {
        "demo": True,
        "reports": [
            {"id": "bt-20260623", "name": "MA动量轮动回测报告", "type": "backtest", "createdAt": "2026-06-23 10:30", "size": "428KB", "status": "ready"},
            {"id": "risk-20260623", "name": "组合风险日报", "type": "risk", "createdAt": "2026-06-23 15:10", "size": "216KB", "status": "ready"},
            {"id": "sig-20260623", "name": "信号中心导出", "type": "signal", "createdAt": "2026-06-23 15:30", "size": "88KB", "status": "ready"},
        ]
    }


def get_demo_data_center() -> dict:
    return {
        "demo": True,
        "sources": [
            {"name": "AKShare", "status": "online", "latency": "320ms", "coverage": "A股/ETF/指数"},
            {"name": "Yahoo Chart", "status": "online", "latency": "180ms", "coverage": "美股/ETF"},
            {"name": "Local CSV", "status": "ready", "latency": "-", "coverage": "本地导入"},
        ],
        "datasets": [
            {"name": "etf_close.parquet", "rows": 9900, "symbols": 11, "start": "2020-01-02", "end": "2026-06-22", "quality": 98},
            {"name": "market_data.duckdb", "rows": 18420, "symbols": 8, "start": "2023-01-01", "end": "2026-06-23", "quality": 96},
        ],
        "quality": [
            {"check": "缺失值", "status": "pass", "value": "0.3%"},
            {"check": "重复日期", "status": "pass", "value": "0"},
            {"check": "价格为0", "status": "pass", "value": "0"},
            {"check": "异常涨跌幅", "status": "watch", "value": "3"},
        ],
    }


def get_demo_strategy_lab() -> dict:
    return {
        "demo": True,
        "strategies": [
            {"id": "ma-cross", "name": "MA Cross", "type": "趋势", "status": "可运行", "lastRun": "2026-06-23 14:20", "sharpe": 1.64},
            {"id": "rsi-reversal", "name": "RSI Reversal", "type": "反转", "status": "观察", "lastRun": "2026-06-22 16:02", "sharpe": 1.12},
            {"id": "sector-rotation", "name": "行业动量轮动", "type": "轮动", "status": "可运行", "lastRun": "2026-06-23 09:40", "sharpe": 1.76},
        ],
        "code": "class Strategy:\\n    name = 'MA Cross'\\n\\n    def on_bar(self, context, bar):\\n        # demo strategy preview\\n        pass\\n",
        "params": [
            {"name": "fast_window", "label": "快线周期", "value": 10, "min": 5, "max": 60},
            {"name": "slow_window", "label": "慢线周期", "value": 30, "min": 20, "max": 240},
            {"name": "stop_loss", "label": "止损比例", "value": 0.08, "min": 0.02, "max": 0.2},
        ],
        "runs": get_demo_backtest()["logs"],
    }


def get_demo_settings() -> dict:
    return {
        "projectRoot": "/Users/qml/Desktop/workspace/quant-fund-lab",
        "dataDir": "data/",
        "reportsDir": "reports/",
        "defaultMarket": "A股ETF",
        "defaultSymbol": "510300",
        "backendVersion": "0.1.0",
        "frontendVersion": "0.1.0",
        "tokens": [{"name": "TUSHARE_TOKEN", "configured": False}],
        "dependencies": [{"name": name, "status": "ok"} for name in ["fastapi", "pandas", "duckdb", "akshare", "yfinance"]],
    }
