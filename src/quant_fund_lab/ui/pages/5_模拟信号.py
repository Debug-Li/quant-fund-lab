from __future__ import annotations

import streamlit as st

from quant_fund_lab.ui.components.logs import render_service_result
from quant_fund_lab.ui.components.tables import render_dataframe, render_dataframe_download
from quant_fund_lab.ui.services.signal_service import generate_latest_signal_service
from quant_fund_lab.ui.services.task_runner import run_task
from quant_fund_lab.ui.state import init_page


init_page("模拟信号")
st.title("模拟信号")

if st.button("生成最新模拟调仓信号", type="primary"):
    with st.spinner("正在生成信号..."):
        st.session_state["signal_result"] = run_task("生成最新模拟信号", generate_latest_signal_service)

result = st.session_state.get("signal_result")
render_service_result(result, show_detail=True)

if result and result.dataframe is not None:
    df = result.dataframe
    styled = df.style.apply(lambda row: ["background-color: #e8f5e9" if row.get("target_weight", 0) > 0 else "" for _ in row], axis=1)
    st.dataframe(styled, use_container_width=True)
    render_dataframe_download(df, "latest_signal.csv")
    if result.files:
        st.caption(f"已保存: {result.files[0]}")
