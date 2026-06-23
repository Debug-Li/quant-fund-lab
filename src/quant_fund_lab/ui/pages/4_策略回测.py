from __future__ import annotations

import datetime as dt

import streamlit as st

from quant_fund_lab.ui.components.charts import render_drawdown_curve
from quant_fund_lab.ui.components.logs import render_service_result
from quant_fund_lab.ui.components.metrics import render_metric_cards
from quant_fund_lab.ui.components.tables import render_dataframe, render_dataframe_download
from quant_fund_lab.ui.services.market_backtest_service import (
    list_available_market_strategies_service,
    run_demo_ma_cross_service,
    run_market_strategy_service,
)
from quant_fund_lab.ui.services.task_runner import run_task
from quant_fund_lab.ui.state import init_page


init_page("策略回测")
st.title("策略回测")

strategy_result = list_available_market_strategies_service()
source = st.radio("数据来源", ["演示数据", "已下载行情"], horizontal=True)
strategy_names = strategy_result.dataframe["strategy"].tolist() if strategy_result.success and strategy_result.dataframe is not None else ["ma_cross"]
strategy_name = st.selectbox("策略", strategy_names)

col1, col2, col3 = st.columns(3)
initial_cash = col1.number_input("初始资金", min_value=1000.0, value=100000.0, step=1000.0)
commission_rate = col2.number_input("手续费率", min_value=0.0, value=0.0003, step=0.0001, format="%.5f")
slippage_rate = col3.number_input("滑点率", min_value=0.0, value=0.0002, step=0.0001, format="%.5f")

if source == "已下载行情":
    symbol = st.text_input("Symbol", value="SPY")
    market = st.selectbox("市场", ["us", "a股", "etf", "index", "crypto"])
    start = st.date_input("开始日期", value=dt.date(2023, 1, 1))
    end = st.date_input("结束日期", value=dt.date.today())
else:
    symbol = market = start = end = None

if st.button("运行策略回测", type="primary"):
    with st.spinner("正在运行策略回测..."):
        if source == "演示数据":
            st.session_state["market_backtest_result"] = run_task(
                "MA Cross 演示回测",
                run_demo_ma_cross_service,
                initial_cash,
                commission_rate,
                slippage_rate,
            )
        else:
            st.session_state["market_backtest_result"] = run_task(
                "本地行情策略回测",
                run_market_strategy_service,
                symbol,
                market,
                str(start),
                str(end),
                strategy_name,
                initial_cash,
                commission_rate,
                slippage_rate,
            )

result = st.session_state.get("market_backtest_result")
render_service_result(result, show_detail=True)

if result and result.success and result.data:
    backtest_result = result.data["result"]
    render_metric_cards(backtest_result.metrics)
    equity = result.data["equity"]
    render_dataframe(equity, "权益曲线数据")
    render_drawdown_curve(equity)
    orders = result.data["orders"]
    render_dataframe(orders, "订单记录")
    render_dataframe_download(orders, "orders.csv")
