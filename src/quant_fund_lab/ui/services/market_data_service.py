from __future__ import annotations

import pandas as pd

from quant_fund_lab.market.indicators.bollinger import bollinger_bands
from quant_fund_lab.market.indicators.ma import moving_average
from quant_fund_lab.market.indicators.macd import macd
from quant_fund_lab.market.indicators.rsi import rsi
from quant_fund_lab.market.services.data_service import fetch_save_and_query
from quant_fund_lab.ui.services.result import ServiceResult


def fetch_market_bars_service(
    symbol: str,
    market: str,
    start: str,
    end: str | None,
    timeframe: str,
    csv_path: str | None = None,
) -> ServiceResult:
    try:
        bars = fetch_save_and_query(symbol, market, start, end, timeframe, csv_path)
        return ServiceResult(True, f"已获取并保存 {symbol} 行情，共 {len(bars)} 行", dataframe=bars, data=bars)
    except Exception as exc:
        message = f"获取行情失败: {exc}"
        if market in {"a股指数", "akshare_index", "cn_index"}:
            message += "。A股指数当前依赖 AKShare 的东方财富接口，若网络或代理异常，可先改用对应 ETF 代码继续研究。"
        return ServiceResult(False, message, error_detail=repr(exc))


def add_indicators_service(bars: pd.DataFrame, indicators: list[str]) -> ServiceResult:
    if bars is None or bars.empty:
        return ServiceResult(False, "没有可计算指标的行情数据。")
    try:
        df = bars.copy()
        selected = set(indicators)
        if "MA" in selected:
            for window in [5, 10, 20, 60]:
                df[f"ma_{window}"] = moving_average(df, window)
        if "RSI" in selected:
            df["rsi"] = rsi(df)
        if "MACD" in selected:
            macd_df = macd(df)
            df = pd.concat([df, macd_df], axis=1)
        if "Bollinger" in selected:
            bands = bollinger_bands(df).rename(
                columns={"upper": "bb_upper", "middle": "bb_middle", "lower": "bb_lower"}
            )
            df = pd.concat([df, bands], axis=1)
        return ServiceResult(True, f"已计算指标: {', '.join(indicators) or '无'}", dataframe=df, data=df)
    except Exception as exc:
        return ServiceResult(False, f"计算指标失败: {exc}", error_detail=repr(exc))
