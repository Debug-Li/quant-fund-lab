from __future__ import annotations

import datetime as dt

import plotly.graph_objects as go
import streamlit as st

from quant_fund_lab.ui.components.charts import render_candlestick, render_volume
from quant_fund_lab.ui.components.logs import render_service_result
from quant_fund_lab.ui.components.tables import render_dataframe, render_dataframe_download
from quant_fund_lab.ui.services.market_data_service import add_indicators_service, fetch_market_bars_service
from quant_fund_lab.ui.services.task_runner import run_task
from quant_fund_lab.ui.state import init_page


init_page("看盘中心")
st.title("看盘中心")
st.caption("示例：`SPY + us`、`000001 + a股股票`、`510300 + a股ETF`、`000300 + a股指数`")

with st.sidebar:
    symbol = st.text_input("Symbol", value="SPY")
    market = st.selectbox("市场", ["us", "a股股票", "a股ETF", "a股指数", "etf", "index", "crypto", "csv"])
    timeframe = st.selectbox("周期", ["1d", "1wk", "1mo"])
    start = st.date_input("开始日期", value=dt.date(2023, 1, 1))
    end = st.date_input("结束日期", value=dt.date.today())
    csv_path = st.text_input("CSV 路径", value="") if market == "csv" else None
    indicators = st.multiselect("技术指标", ["MA", "RSI", "MACD", "Bollinger"], default=["MA"])
    fetch_clicked = st.button("获取数据", use_container_width=True)

if fetch_clicked:
    with st.spinner("正在获取行情..."):
        bars_result = run_task(
            "获取行情",
            fetch_market_bars_service,
            symbol,
            market,
            str(start),
            str(end),
            timeframe,
            csv_path or None,
        )
    render_service_result(bars_result, show_detail=True)
    if bars_result.success:
        ind_result = run_task("计算指标", add_indicators_service, bars_result.dataframe, indicators)
        st.session_state["market_result"] = ind_result
else:
    ind_result = st.session_state.get("market_result")

render_service_result(ind_result, show_detail=True)

if ind_result and ind_result.dataframe is not None:
    df = ind_result.dataframe
    render_candlestick(df, f"{symbol} K 线")
    render_volume(df)
    if "rsi" in df:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df["datetime"], y=df["rsi"], mode="lines", name="RSI"))
        fig.update_layout(title="RSI", height=260)
        st.plotly_chart(fig, use_container_width=True)
    if {"macd", "signal", "histogram"}.issubset(df.columns):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df["datetime"], y=df["macd"], mode="lines", name="MACD"))
        fig.add_trace(go.Scatter(x=df["datetime"], y=df["signal"], mode="lines", name="Signal"))
        fig.add_trace(go.Bar(x=df["datetime"], y=df["histogram"], name="Histogram"))
        fig.update_layout(title="MACD", height=300)
        st.plotly_chart(fig, use_container_width=True)
    render_dataframe(df.tail(200), "行情表格")
    render_dataframe_download(df, f"{symbol}_bars.csv")
