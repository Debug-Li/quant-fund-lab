from __future__ import annotations

import pandas as pd
import streamlit as st

from quant_fund_lab.ui.config import (
    LATEST_SIGNAL_PATH,
    PROCESSED_PRICE_PATH,
    RAW_PRICE_PATH,
    ROTATION_STATS_PATH,
    UI_TITLE,
    path_status,
)
from quant_fund_lab.ui.components.layout import render_risk_notice
from quant_fund_lab.ui.state import init_page


init_page(UI_TITLE)

st.title("Quant Fund Lab")
st.caption("本地看盘与量化研究工作台")

st.markdown(
    """
这个 UI 把原先命令行里的数据获取、ETF 轮动回测、轻量策略回测、模拟信号和报告查看整合到本地浏览器页面中。

推荐工作流：

```text
数据中心 -> 看盘中心 -> 轮动回测 / 策略回测 -> 模拟信号 -> 报告中心
```
"""
)

render_risk_notice()

st.subheader("数据与报告状态")
status_df = pd.DataFrame(
    [
        {"name": "raw ETF data", **path_status(RAW_PRICE_PATH)},
        {"name": "processed close matrix", **path_status(PROCESSED_PRICE_PATH)},
        {"name": "rotation stats", **path_status(ROTATION_STATS_PATH)},
        {"name": "latest signal", **path_status(LATEST_SIGNAL_PATH)},
    ]
)
st.dataframe(status_df, use_container_width=True)

st.subheader("页面导航")
st.markdown(
    """
- **数据中心**：生成演示数据、下载 AKShare ETF 研究池数据、预览本地 Parquet。
- **看盘中心**：拉取单标的行情，展示 K 线、成交量和技术指标。
- **轮动回测**：运行指数/行业 ETF 动量轮动回测。
- **策略回测**：运行 MA Cross 等轻量单标的策略回测。
- **模拟信号**：生成最新一期目标权重与调仓信号。
- **报告中心**：预览和下载 `reports/` 下的产物。
- **设置诊断**：检查路径、依赖和运行命令。
"""
)
