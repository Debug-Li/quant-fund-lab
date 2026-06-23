# 量观 Quant Lab

量观 Quant Lab 是一个本地运行的专业量化研究、看盘、回测、组合管理与风险监控平台。当前主线已经从命令行研究工具升级为 `FastAPI + React + Vite + TypeScript + ECharts` 的本地金融终端。

默认路线是：

```text
数据获取 -> 数据落地 -> 策略研究 -> 组合回测 -> 每日/每周模拟信号
AKShare    Parquet     Pandas      bt         本地信号脚本
```

## 启动量观 Quant Lab

一键启动后端和前端：

```bash
cd /Users/qml/Desktop/workspace/quant-fund-lab
uv run quant-lab
```

也可以分别启动：

```bash
uv run quant-lab-api
```

```bash
cd apps/web
npm install
npm run dev
```

打开：

```text
http://localhost:5173
```

页面包括：

- 总览
- 市场看盘
- 策略研究
- 回测分析
- 组合管理
- 信号中心
- 数据中心
- 风险监控
- 报告中心
- 设置

所有页面都内置 demo 数据，即使没有真实行情或网络也可以完整渲染。平台不默认接入真实交易下单。

## 环境

项目使用 `uv` 管理 Python 3.12 和依赖。

```bash
cd /Users/qml/Desktop/workspace/quant-fund-lab
uv run python --version
uv run jupyter lab
```

## Legacy Streamlit UI

旧版 Streamlit UI 仍保留给开发调试：

```bash
uv run qfl-ui
```

或：

```bash
uv run streamlit run src/quant_fund_lab/ui/streamlit_app.py
```

启动后在浏览器中使用：

- 数据中心：生成演示数据或下载 AKShare ETF 研究池数据
- 看盘中心：拉取单标的行情、查看 K 线和技术指标
- 轮动回测：运行 ETF 动量轮动策略
- 策略回测：运行轻量单标的策略回测
- 模拟信号：生成最新一期模拟调仓信号
- 报告中心：查看和下载报告文件
- 设置诊断：检查路径、依赖和数据状态

旧命令行入口仍保留给开发调试，但普通用户推荐使用 UI。

## 开发者命令

下载默认 ETF 研究池数据：

```bash
uv run qfl-data
```

如果当前网络连不上 AKShare/东方财富接口，可以先生成演示数据验证流程：

```bash
uv run qfl-demo-data
```

运行行业/指数动量轮动回测：

```bash
uv run qfl-backtest
```

生成最新一期模拟调仓信号：

```bash
uv run qfl-signal
```

运行需求文档中的轻量回测内核演示：

```bash
uv run qfl-market-demo
```

启动应用核心入口：

```bash
uv run python app/main.py
```

运行测试：

```bash
uv run pytest
```

macOS 双击快捷启动：

```text
启动量化.command
```

也可以在终端中指定动作：

```bash
./启动量化.command jupyter
./启动量化.command ui
./启动量化.command app
./启动量化.command test
```

如果脚本因为数据源网络波动失败，稍后重试即可。AKShare 数据来自公开网页接口，适合学习和研究，不建议直接作为实盘唯一依据。

## 目录

```text
configs/                  基金/ETF 研究池配置
data/raw/                 原始下载数据
data/processed/           清洗后的价格数据
data/features/            指标和因子数据
notebooks/                Jupyter 研究笔记
reports/                  回测图表和信号输出
src/quant_fund_lab/       项目代码
```

## 默认策略

当前内置的是一个很朴素的动量轮动策略：

- 使用 `configs/universe.yml` 中的 ETF 研究池
- 每月调仓一次
- 用过去 60 个交易日收益率作为动量分数
- 持有排名靠前的 3 只基金
- 等权配置
- 可设置 20 日均线作为趋势过滤

这不是投资建议，只是一个学习模板。后续可以继续加入估值、波动率、最大回撤、行业拥挤度、股债切换等模块。

## 看盘与量化研究 MVP 开发进度

已根据《看盘与量化研究软件需求文档 v0.1》完成第一批内核模块：

- `app/main.py`：应用核心启动入口。
- `market/data/providers/`：`BaseDataProvider`、`YFinanceProvider`、`AKShareProvider`、`CSVProvider`。
- `market/data/storage/`：DuckDB 初始化、行情保存、按 symbol/日期/周期查询、重复数据替换。
- `market/indicators/`：MA、RSI、MACD、Bollinger Bands。
- `market/strategies/`：统一 `Strategy` 接口、策略加载器、示例策略。
- `market/backtest/`：单标的、日线、无杠杆轻量回测引擎，支持下一根开盘成交、手续费、滑点、买入、卖出、清仓、权益曲线和指标。
- `tests/`：覆盖指标、数据存储、策略加载、回测撮合和边界价格。

下一步是 PySide6 桌面界面：主看盘页、指标勾选、策略编辑器和回测报告页。
当前已按新规划优先实现 Streamlit 本地浏览器 UI，PySide6 可作为后续原生桌面方向。
