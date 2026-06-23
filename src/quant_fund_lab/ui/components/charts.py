from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def render_price_line(df: pd.DataFrame, date_col: str = "date", value_col: str = "close", title: str = "价格走势") -> None:
    if df is None or df.empty:
        st.info("暂无价格数据")
        return
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df[date_col], y=df[value_col], mode="lines", name=value_col))
    fig.update_layout(title=title, height=420, margin=dict(l=20, r=20, t=50, b=20))
    st.plotly_chart(fig, use_container_width=True)


def render_price_matrix(prices: pd.DataFrame, title: str = "ETF 净值/收盘价矩阵") -> None:
    if prices is None or prices.empty:
        st.info("暂无价格矩阵")
        return
    normalized = prices / prices.iloc[0]
    fig = go.Figure()
    for column in normalized.columns:
        fig.add_trace(go.Scatter(x=normalized.index, y=normalized[column], mode="lines", name=str(column)))
    fig.update_layout(title=title, height=460, margin=dict(l=20, r=20, t=50, b=20))
    st.plotly_chart(fig, use_container_width=True)


def render_drawdown_curve(equity: pd.DataFrame | pd.Series, title: str = "回撤曲线") -> None:
    if equity is None or len(equity) == 0:
        st.info("暂无权益数据")
        return
    if isinstance(equity, pd.DataFrame):
        if "total_equity" in equity:
            series = equity["total_equity"]
            x_values = equity["datetime"] if "datetime" in equity else equity.index
        else:
            series = equity.iloc[:, 0]
            x_values = equity.index
    else:
        series = equity
        x_values = equity.index
    drawdown = series / series.cummax() - 1
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_values, y=drawdown, mode="lines", fill="tozeroy", name="drawdown"))
    fig.update_layout(title=title, height=320, margin=dict(l=20, r=20, t=50, b=20))
    st.plotly_chart(fig, use_container_width=True)


def render_candlestick(df: pd.DataFrame, title: str = "K线图") -> None:
    if df is None or df.empty:
        st.info("暂无 K 线数据")
        return
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=df["datetime"],
                open=df["open"],
                high=df["high"],
                low=df["low"],
                close=df["close"],
                name="K线",
            )
        ]
    )
    for col in [c for c in df.columns if c.startswith("ma_")]:
        fig.add_trace(go.Scatter(x=df["datetime"], y=df[col], mode="lines", name=col.upper()))
    if {"bb_upper", "bb_middle", "bb_lower"}.issubset(df.columns):
        fig.add_trace(go.Scatter(x=df["datetime"], y=df["bb_upper"], mode="lines", name="BB Upper"))
        fig.add_trace(go.Scatter(x=df["datetime"], y=df["bb_middle"], mode="lines", name="BB Middle"))
        fig.add_trace(go.Scatter(x=df["datetime"], y=df["bb_lower"], mode="lines", name="BB Lower"))
    fig.update_layout(title=title, height=520, xaxis_rangeslider_visible=False, margin=dict(l=20, r=20, t=50, b=20))
    st.plotly_chart(fig, use_container_width=True)


def render_volume(df: pd.DataFrame, title: str = "成交量") -> None:
    if df is None or df.empty or "volume" not in df:
        st.info("暂无成交量数据")
        return
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df["datetime"], y=df["volume"], name="volume"))
    fig.update_layout(title=title, height=260, margin=dict(l=20, r=20, t=50, b=20))
    st.plotly_chart(fig, use_container_width=True)
