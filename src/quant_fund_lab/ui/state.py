from __future__ import annotations

import streamlit as st


def init_page(title: str) -> None:
    st.set_page_config(page_title=title, page_icon="📈", layout="wide")
