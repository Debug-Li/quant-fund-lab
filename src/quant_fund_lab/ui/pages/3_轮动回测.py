from __future__ import annotations

import streamlit as st

from quant_fund_lab.ui.components.logs import render_service_result
from quant_fund_lab.ui.components.tables import render_dataframe, render_dataframe_download
from quant_fund_lab.ui.services.rotation_service import run_rotation_backtest_service
from quant_fund_lab.ui.services.task_runner import run_task
from quant_fund_lab.ui.state import init_page


init_page("轮动回测")
st.title("轮动回测")

col1, col2, col3 = st.columns(3)
lookback_days = col1.number_input("动量窗口", min_value=5, max_value=260, value=60, step=5)
top_n = col2.number_input("持仓数量 Top N", min_value=1, max_value=10, value=3, step=1)
trend_days = col3.number_input("趋势过滤均线", min_value=5, max_value=260, value=20, step=5)

if st.button("运行轮动回测", type="primary"):
    with st.spinner("正在运行轮动回测..."):
        st.session_state["rotation_result"] = run_task(
            "轮动回测",
            run_rotation_backtest_service,
            int(lookback_days),
            int(top_n),
            int(trend_days),
        )

result = st.session_state.get("rotation_result")
render_service_result(result, show_detail=True)

if result and result.dataframe is not None:
    render_dataframe(result.dataframe, "回测统计")
    render_dataframe_download(result.dataframe, "rotation_stats.csv")
    if result.files:
        st.caption(f"已保存: {result.files[0]}")
