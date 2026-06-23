from __future__ import annotations

import streamlit as st

from quant_fund_lab.ui.services.result import ServiceResult


def render_service_result(result: ServiceResult | None, show_detail: bool = False) -> None:
    if result is None:
        return
    if result.success:
        st.success(result.message)
    else:
        st.error(result.message)

    if result.logs:
        with st.expander("运行日志", expanded=False):
            for line in result.logs:
                st.write(line)
    if result.error_detail and show_detail:
        with st.expander("错误详情", expanded=False):
            st.code(result.error_detail)
