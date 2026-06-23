from __future__ import annotations

from pathlib import Path

import streamlit as st

from quant_fund_lab.ui.components.logs import render_service_result
from quant_fund_lab.ui.components.tables import render_dataframe, render_dataframe_download
from quant_fund_lab.ui.services.report_service import list_reports_service, preview_report_service
from quant_fund_lab.ui.state import init_page


init_page("报告中心")
st.title("报告中心")

reports = list_reports_service()
render_service_result(reports, show_detail=True)
render_dataframe(reports.dataframe, "报告文件")

if reports.files:
    selected = st.selectbox("选择报告", [str(path) for path in reports.files])
    preview = preview_report_service(selected)
    render_service_result(preview, show_detail=True)
    if preview.dataframe is not None:
        render_dataframe(preview.dataframe.head(500), "报告预览")
        render_dataframe_download(preview.dataframe, Path(selected).with_suffix(".csv").name)
    with Path(selected).open("rb") as file:
        st.download_button("下载文件", file.read(), file_name=Path(selected).name)
else:
    st.info("暂无报告。可先运行轮动回测或模拟信号。")
