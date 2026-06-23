from __future__ import annotations

import streamlit as st


def render_risk_notice() -> None:
    st.warning("本项目仅用于学习研究，不构成投资建议；数据源可能延迟、缺失或存在复权差异。")
