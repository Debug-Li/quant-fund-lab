from __future__ import annotations

import pandas as pd
import streamlit as st


def render_dataframe(df: pd.DataFrame | None, title: str | None = None) -> None:
    if title:
        st.subheader(title)
    if df is None or df.empty:
        st.info("暂无数据")
        return
    st.dataframe(df, use_container_width=True)


def render_dataframe_download(df: pd.DataFrame | None, filename: str) -> None:
    if df is None or df.empty:
        return
    csv = df.to_csv(index=False).encode("utf-8-sig")
    st.download_button("下载 CSV", csv, file_name=filename, mime="text/csv")
