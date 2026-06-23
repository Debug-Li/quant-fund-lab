from __future__ import annotations

import streamlit as st

from quant_fund_lab.ui.components.charts import render_price_matrix
from quant_fund_lab.ui.components.logs import render_service_result
from quant_fund_lab.ui.components.tables import render_dataframe, render_dataframe_download
from quant_fund_lab.ui.services.fund_data_service import (
    download_live_data_service,
    generate_demo_data_service,
    load_processed_price_matrix_service,
    load_raw_price_data_service,
    load_universe_service,
)
from quant_fund_lab.ui.services.task_runner import run_task
from quant_fund_lab.ui.state import init_page


init_page("数据中心")
st.title("数据中心")

universe = load_universe_service()
render_service_result(universe)
render_dataframe(universe.dataframe, "默认 ETF 研究池")

col1, col2, col3, col4 = st.columns(4)

if col1.button("生成演示数据", use_container_width=True):
    with st.spinner("正在生成演示数据..."):
        st.session_state["data_result"] = run_task("生成演示数据", generate_demo_data_service)

if col2.button("下载真实 AKShare 数据", use_container_width=True):
    with st.spinner("正在下载真实数据..."):
        st.session_state["data_result"] = run_task("下载真实数据", download_live_data_service)

if col3.button("读取 processed 数据", use_container_width=True):
    st.session_state["data_result"] = run_task("读取 processed 数据", load_processed_price_matrix_service)

if col4.button("读取 raw 数据", use_container_width=True):
    st.session_state["data_result"] = run_task("读取 raw 数据", load_raw_price_data_service)

result = st.session_state.get("data_result")
render_service_result(result, show_detail=True)

if result and result.dataframe is not None:
    st.subheader("数据预览")
    render_dataframe(result.dataframe.head(200))
    render_dataframe_download(result.dataframe, "quant_fund_data.csv")
    if result.data is not None and hasattr(result.data, "index") and len(result.data) > 0:
        try:
            render_price_matrix(result.data, "本地 ETF 价格矩阵")
        except Exception:
            pass

if result and result.files:
    st.subheader("文件路径")
    for path in result.files:
        st.code(str(path))
