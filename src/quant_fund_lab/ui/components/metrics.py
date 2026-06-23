from __future__ import annotations

import streamlit as st


def _format_metric(value) -> str:
    if isinstance(value, float):
        return f"{value:.4f}"
    return str(value)


def render_metric_cards(metrics: dict) -> None:
    if not metrics:
        st.info("暂无指标")
        return
    cols = st.columns(min(len(metrics), 4))
    for index, (key, value) in enumerate(metrics.items()):
        cols[index % len(cols)].metric(key, _format_metric(value))
