from __future__ import annotations

import importlib
import platform

import pandas as pd
import streamlit as st

from quant_fund_lab.config.settings import settings
from quant_fund_lab.ui.state import init_page


init_page("设置诊断")
st.title("设置诊断")

st.subheader("运行环境")
st.write(f"项目根目录: `{settings.project_root}`")
st.write(f"Python: `{platform.python_version()}`")

deps = ["akshare", "pandas", "plotly", "bt", "streamlit", "duckdb", "yfinance"]
dep_rows = []
for name in deps:
    try:
        module = importlib.import_module(name)
        dep_rows.append({"dependency": name, "available": True, "version": getattr(module, "__version__", "-")})
    except Exception as exc:
        dep_rows.append({"dependency": name, "available": False, "version": str(exc)})
st.dataframe(pd.DataFrame(dep_rows), use_container_width=True)

st.subheader("关键路径")
paths = [
    settings.project_root / "configs" / "universe.yml",
    settings.project_root / "data" / "raw",
    settings.project_root / "data" / "processed",
    settings.project_root / "reports",
]
st.dataframe(pd.DataFrame({"path": [str(path) for path in paths], "exists": [path.exists() for path in paths]}), use_container_width=True)

st.subheader("脚本入口")
st.code(
    """
uv run qfl-ui
uv run qfl-data
uv run qfl-demo-data
uv run qfl-backtest
uv run qfl-signal
uv run qfl-market-demo
uv run pytest
""".strip()
)

st.warning("本项目仅用于学习研究，不接入真实自动下单。数据源可能存在延迟、缺失或复权差异。")
