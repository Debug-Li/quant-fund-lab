# CODEX 执行文档：quant-fund-lab 前端 UI 化改造

> 目标仓库：`Debug-Li/quant-fund-lab`  
> 建议写入路径：`docs/CODEX_UI_EXECUTION.md`  
> 目标：把当前依赖命令行执行的量化研究流程改造成可视化 UI 工作台，让普通用户通过浏览器页面完成数据获取、看盘、指标展示、轮动回测、轻量策略回测、模拟调仓信号和报告查看。

---

## 1. 当前仓库理解

仓库当前是一个本地量化研究实验室，主要研究指数基金、行业 ETF、行业主题基金和轻量策略回测。

README 中给出的主流程是：

```text
数据获取 -> 数据落地 -> 策略研究 -> 组合回测 -> 每日/每周模拟信号
AKShare    Parquet     Pandas      bt         本地信号脚本
```

当前项目使用：

- Python 3.12
- uv 依赖管理
- AKShare 获取基金/ETF 数据
- Parquet 落地数据
- pandas / numpy 处理数据
- bt 做 ETF 轮动组合回测
- 自研 `market` 轻量单标的回测内核
- pytest 做测试

当前用户入口仍以命令行为主，本次任务是新增 UI 并将现有能力嵌入页面。

---

## 2. 当前关键目录结构

当前仓库核心结构如下：

```text
quant-fund-lab/
  app/
    main.py

  configs/
    universe.yml

  docs/
    网页版协同决策记录.md

  notebooks/
  reports/
  strategies/
  tests/

  src/quant_fund_lab/
    backtest/
      rotation_bt.py

    config/
      settings.py

    data/
      akshare_loader.py
      download_sample.py

    features/
      momentum.py

    market/
      backtest/
        broker.py
        engine.py
        metrics.py
        portfolio.py
        report.py
      data/
        models.py
        providers/
        storage/
      indicators/
        ma.py
        rsi.py
        macd.py
        bollinger.py
      services/
        data_service.py
        backtest_service.py
        strategy_service.py
      strategies/
        base.py
        loader.py
        examples/

    simulate/
      daily_signal.py

    strategies/
    utils/
      exceptions.py
      logger.py
```

UI 新代码应放在 `src/quant_fund_lab/ui/` 下，不建议放到根目录 `app/ui/`，因为当前主要业务代码都在 `src/quant_fund_lab/` 包内。根目录 `app/main.py` 可以继续作为核心启动入口保留。

---

## 3. 当前命令行入口与 UI 映射

当前 `pyproject.toml` 中已有脚本入口：

| 旧命令 | 当前函数入口 | 当前作用 | UI 页面 |
|---|---|---|---|
| `uv run qfl-data` | `quant_fund_lab.data.download_sample:main` | 从 AKShare 下载默认 ETF 研究池数据，保存 raw 和 processed Parquet | 数据中心 |
| `uv run qfl-demo-data` | `quant_fund_lab.data.download_sample:demo_main` | 生成演示行情数据，保存到本地 Parquet | 数据中心 |
| `uv run qfl-backtest` | `quant_fund_lab.backtest.rotation_bt:main` | 运行行业/指数动量轮动回测，输出 `reports/rotation_stats.csv` | 轮动回测 |
| `uv run qfl-signal` | `quant_fund_lab.simulate.daily_signal:main` | 生成最新一期模拟调仓信号，输出 `reports/latest_signal.csv` | 模拟信号 |
| `uv run qfl-market-demo` | `quant_fund_lab.market.services.backtest_service:main` | 运行轻量单标的 MA Cross 回测演示 | 策略回测 |
| `uv run python app/main.py` | `app/main.py` | 应用核心入口 | 保留，不作为普通用户主入口 |
| `uv run pytest` | pytest | 测试 | 设置/诊断页可显示测试说明，不直接强制运行 |

改造后，用户主入口应变为：

```bash
uv run qfl-ui
```

或：

```bash
uv run streamlit run src/quant_fund_lab/ui/streamlit_app.py
```

旧 CLI 保留给开发者调试，但 README 中应把 UI 作为推荐使用方式。

---

## 4. UI 技术方案

第一版使用 Streamlit。

原因：

1. 当前项目是 Python 量化研究项目，Streamlit 可直接复用 pandas、Plotly 和现有 service 函数。
2. 仓库已依赖 Plotly，适合快速做净值曲线、回撤曲线、K 线和指标图。
3. 当前目标是摆脱命令行，不是做正式多用户 SaaS，因此不需要一开始引入 FastAPI + React 的重架构。
4. UI 可以本地浏览器运行，适合个人量化研究工作流。

需要新增依赖：

```toml
streamlit>=1.0
```

如果 Codex 发现项目当前用 `uv.lock` 管理依赖，应通过：

```bash
uv add streamlit
```

不要手动只改 `pyproject.toml` 而不更新 lock 文件。

---

## 5. 新增目标目录

请新增：

```text
src/quant_fund_lab/ui/
  __init__.py
  streamlit_app.py
  launcher.py
  state.py
  config.py

  services/
    __init__.py
    result.py
    task_runner.py
    fund_data_service.py
    rotation_service.py
    signal_service.py
    market_data_service.py
    market_backtest_service.py
    report_service.py

  components/
    __init__.py
    layout.py
    charts.py
    tables.py
    metrics.py
    logs.py
    forms.py

  pages/
    1_数据中心.py
    2_看盘中心.py
    3_轮动回测.py
    4_策略回测.py
    5_模拟信号.py
    6_报告中心.py
    7_设置诊断.py
```

同时在 `docs/` 中加入本执行文档：

```text
docs/CODEX_UI_EXECUTION.md
```

---

## 6. ServiceResult 统一返回协议

新增：`src/quant_fund_lab/ui/services/result.py`

```python
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pandas as pd


@dataclass
class ServiceResult:
    success: bool
    message: str
    data: Any | None = None
    dataframe: pd.DataFrame | None = None
    files: list[Path] = field(default_factory=list)
    logs: list[str] = field(default_factory=list)
    error_detail: str | None = None
```

要求：

1. UI 页面只消费 `ServiceResult`。
2. service 内部捕获异常并返回 `success=False`。
3. 不要让 Streamlit 页面直接调用 `print()` 或直接写复杂业务逻辑。
4. 旧 CLI 可以继续 `print()`，但应优先调用 service 函数。

---

## 7. 任务运行封装

新增：`src/quant_fund_lab/ui/services/task_runner.py`

```python
from __future__ import annotations

import traceback
from collections.abc import Callable
from typing import Any

from quant_fund_lab.ui.services.result import ServiceResult


def run_task(name: str, func: Callable[..., ServiceResult], *args: Any, **kwargs: Any) -> ServiceResult:
    try:
        result = func(*args, **kwargs)
        result.logs.insert(0, f"任务完成: {name}")
        return result
    except Exception as exc:
        return ServiceResult(
            success=False,
            message=f"任务失败: {name}: {exc}",
            error_detail=traceback.format_exc(),
            logs=[f"任务失败: {name}"],
        )
```

Streamlit 页面中使用 `st.spinner()` 包裹 `run_task()`。

---

## 8. 页面一：首页 Dashboard

文件：`src/quant_fund_lab/ui/streamlit_app.py`

功能：

1. 设置页面标题：`Quant Fund Lab`。
2. 显示项目说明。
3. 显示当前数据目录状态：
   - `data/raw/etf_daily.parquet` 是否存在
   - `data/processed/etf_close.parquet` 是否存在
   - `reports/rotation_stats.csv` 是否存在
   - `reports/latest_signal.csv` 是否存在
4. 显示导航说明：
   - 数据中心
   - 看盘中心
   - 轮动回测
   - 策略回测
   - 模拟信号
   - 报告中心
   - 设置诊断
5. 提醒：本项目仅用于学习研究，不构成投资建议。

---

## 9. 页面二：数据中心

文件：`src/quant_fund_lab/ui/pages/1_数据中心.py`

接入当前能力：

- `quant_fund_lab.data.download_sample.build_demo_prices`
- `quant_fund_lab.data.download_sample.save_price_data`
- `quant_fund_lab.data.download_sample.main` 中的 AKShare 下载逻辑
- `quant_fund_lab.data.akshare_loader.load_universe`
- `quant_fund_lab.data.akshare_loader.fetch_universe_prices`
- `quant_fund_lab.data.akshare_loader.to_price_matrix`

建议新增 service：`src/quant_fund_lab/ui/services/fund_data_service.py`

需要提供：

```python
def load_universe_service() -> ServiceResult: ...
def generate_demo_data_service() -> ServiceResult: ...
def download_live_data_service() -> ServiceResult: ...
def load_processed_price_matrix_service() -> ServiceResult: ...
def load_raw_price_data_service() -> ServiceResult: ...
```

页面控件：

1. 显示 `configs/universe.yml` 的研究池表格。
2. 按钮：生成演示数据。
3. 按钮：下载真实 AKShare 数据。
4. 按钮：读取本地 processed 数据。
5. 按钮：读取本地 raw 数据。
6. 数据预览表格。
7. 下载 CSV 按钮。
8. 显示 raw 和 processed 文件路径。

验收标准：

1. 不用执行 `uv run qfl-data`，页面可下载并保存数据。
2. 不用执行 `uv run qfl-demo-data`，页面可生成演示数据。
3. 页面能显示 `etf_close.parquet` 的矩阵形状和前几行。
4. 数据源网络失败时显示友好错误，并提示用户可先用演示数据。

---

## 10. 页面三：看盘中心

文件：`src/quant_fund_lab/ui/pages/2_看盘中心.py`

接入当前能力：

- `quant_fund_lab.market.services.data_service.provider_for_market`
- `quant_fund_lab.market.services.data_service.fetch_save_and_query`
- `quant_fund_lab.market.indicators.ma`
- `quant_fund_lab.market.indicators.rsi`
- `quant_fund_lab.market.indicators.macd`
- `quant_fund_lab.market.indicators.bollinger`
- `quant_fund_lab.market.data.storage.market_data_repository.MarketDataRepository`

建议新增 service：`src/quant_fund_lab/ui/services/market_data_service.py`

需要提供：

```python
def fetch_market_bars_service(
    symbol: str,
    market: str,
    start: str,
    end: str | None,
    timeframe: str,
    csv_path: str | None = None,
) -> ServiceResult: ...


def add_indicators_service(
    bars: pd.DataFrame,
    indicators: list[str],
) -> ServiceResult: ...
```

页面控件：

1. symbol 输入框，默认 `SPY` 或 `510300`。
2. 市场选择：`us`、`a股`、`etf`、`index`、`crypto`、`csv`。
3. 日期范围。
4. 周期选择，默认 `1d`。
5. CSV 路径输入，仅当 market 为 `csv` 时显示。
6. 指标勾选：MA、RSI、MACD、Bollinger。
7. 获取数据按钮。
8. 原始 K 线表格。
9. Plotly K 线图或折线图。
10. 成交量图。
11. 指标图。

验收标准：

1. 用户无需命令行即可拉取并查看单标的行情。
2. 支持至少 MA、RSI、MACD、Bollinger 中的已有指标展示。
3. 拉取数据后保存到本地 DuckDB，并能从 repository 查询。
4. 出错时显示 `DataProviderError` 的用户友好提示。

---

## 11. 页面四：轮动回测

文件：`src/quant_fund_lab/ui/pages/3_轮动回测.py`

接入当前能力：

- `quant_fund_lab.backtest.rotation_bt.load_price_matrix`
- `quant_fund_lab.backtest.rotation_bt.build_strategy`
- `quant_fund_lab.backtest.rotation_bt.run_backtest`
- `quant_fund_lab.features.momentum.momentum_score`
- `quant_fund_lab.features.momentum.top_n_selection`
- `quant_fund_lab.features.momentum.trend_mask`

当前 `rotation_bt.run_backtest(prices)` 会从 `configs/universe.yml` 读取参数。为了 UI 可调参，请非破坏性新增：

```python
def run_backtest_with_params(
    prices: pd.DataFrame,
    lookback_days: int = 60,
    top_n: int = 3,
    trend_days: int = 20,
) -> bt.backtest.Result:
    strategy = build_strategy(
        prices=prices,
        lookback_days=lookback_days,
        top_n=top_n,
        trend_days=trend_days,
    )
    test = bt.Backtest(strategy, prices)
    return bt.run(test)
```

保留原 `run_backtest(prices)` 不变，避免破坏 CLI。

建议新增 service：`src/quant_fund_lab/ui/services/rotation_service.py`

需要提供：

```python
def run_rotation_backtest_service(
    lookback_days: int,
    top_n: int,
    trend_days: int,
) -> ServiceResult: ...
```

页面控件：

1. 加载本地 ETF close matrix。
2. 参数：lookback_days，默认 60。
3. 参数：top_n，默认 3。
4. 参数：trend_days，默认 20。
5. 按钮：运行轮动回测。
6. 显示 bt 结果统计表 `result.stats`。
7. 保存并提供下载 `reports/rotation_stats.csv`。
8. 如果能从 bt 结果提取净值序列，则显示净值曲线和回撤曲线。

验收标准：

1. 不执行 `uv run qfl-backtest` 也能在页面运行同等回测。
2. 页面参数能覆盖配置文件默认参数。
3. 仍然生成 `reports/rotation_stats.csv`。
4. 如果没有 processed 数据，提示先到“数据中心”生成或下载数据。

---

## 12. 页面五：策略回测

文件：`src/quant_fund_lab/ui/pages/4_策略回测.py`

接入当前能力：

- `quant_fund_lab.market.services.backtest_service.make_demo_bars`
- `quant_fund_lab.market.services.backtest_service.run_backtest`
- `quant_fund_lab.market.services.backtest_service.run_example_backtest`
- `quant_fund_lab.market.strategies.loader`
- `quant_fund_lab.market.strategies.examples.ma_cross`
- `quant_fund_lab.market.backtest.engine.BacktestEngine`
- `quant_fund_lab.market.backtest.report`

建议新增 service：`src/quant_fund_lab/ui/services/market_backtest_service.py`

需要提供：

```python
def list_available_market_strategies_service() -> ServiceResult: ...
def run_demo_ma_cross_service(initial_cash: float, commission_rate: float, slippage_rate: float) -> ServiceResult: ...
def run_market_strategy_service(symbol: str, market: str, start: str, end: str, strategy_name: str, initial_cash: float, commission_rate: float, slippage_rate: float) -> ServiceResult: ...
```

页面控件：

1. 数据来源：演示数据 / 已下载行情。
2. strategy 选择，第一版至少支持 MA Cross。
3. 初始资金。
4. 手续费率。
5. 滑点率。
6. 运行按钮。
7. 指标卡片：总收益、年化收益、最大回撤、夏普、交易次数等，以 `result.metrics` 为准。
8. 订单表：`result.orders`。
9. 交易表，如果引擎已有。
10. 权益曲线：`result.equity_curve` 或报告对象中的权益数据。

验收标准：

1. 不执行 `uv run qfl-market-demo` 也能通过 UI 跑 MA Cross 示例。
2. 页面展示 metrics 和 orders 数量。
3. 参数调整后结果变化。
4. 策略报错时显示错误原因。

---

## 13. 页面六：模拟信号

文件：`src/quant_fund_lab/ui/pages/5_模拟信号.py`

接入当前能力：

- `quant_fund_lab.simulate.daily_signal.load_price_matrix`
- `quant_fund_lab.simulate.daily_signal.latest_signal`

建议新增 service：`src/quant_fund_lab/ui/services/signal_service.py`

需要提供：

```python
def generate_latest_signal_service() -> ServiceResult: ...
```

页面控件：

1. 按钮：生成最新模拟调仓信号。
2. 表格显示：date、fund、close、momentum、eligible、target_weight。
3. 高亮 target_weight > 0 的目标持仓。
4. 保存并提供下载 `reports/latest_signal.csv`。

验收标准：

1. 不执行 `uv run qfl-signal` 也能通过页面生成信号。
2. 页面能显示完整信号表。
3. 如果缺少 `etf_close.parquet`，提示先到数据中心生成/下载数据。

---

## 14. 页面七：报告中心

文件：`src/quant_fund_lab/ui/pages/6_报告中心.py`

建议新增 service：`src/quant_fund_lab/ui/services/report_service.py`

功能：

1. 扫描 `reports/` 目录。
2. 展示所有 `.csv`、`.html`、`.png`、`.jpg`、`.parquet` 文件。
3. 对 `rotation_stats.csv` 做表格预览。
4. 对 `latest_signal.csv` 做表格预览。
5. 提供下载按钮。
6. 后续如有 quantstats HTML 报告，也可直接提供下载。

验收标准：

1. 已生成的报告能在页面中看到。
2. CSV 能直接预览。
3. 文件不存在时不报错，显示“暂无报告”。

---

## 15. 页面八：设置诊断

文件：`src/quant_fund_lab/ui/pages/7_设置诊断.py`

功能：

1. 显示项目根目录。
2. 显示 Python 版本。
3. 显示关键依赖是否可导入：akshare、pandas、plotly、bt、streamlit、duckdb、yfinance。
4. 显示关键路径是否存在：
   - configs/universe.yml
   - data/raw/
   - data/processed/
   - reports/
5. 显示当前脚本入口映射。
6. 显示风险提示：数据源仅用于学习研究，不应作为实盘唯一依据。

不要在 UI 中直接执行 pytest，避免用户误点造成长时间卡顿。可以显示命令：

```bash
uv run pytest
```

---

## 16. 组件封装要求

### 16.1 charts.py

新增：`src/quant_fund_lab/ui/components/charts.py`

至少提供：

```python
def render_price_line(df, date_col="date", value_col="close", title="价格走势"): ...
def render_price_matrix(prices, title="ETF 净值/收盘价矩阵"): ...
def render_drawdown_curve(equity, title="回撤曲线"): ...
def render_candlestick(df, title="K线图"): ...
def render_volume(df, title="成交量"): ...
```

优先使用 Plotly。

### 16.2 tables.py

新增：`src/quant_fund_lab/ui/components/tables.py`

至少提供：

```python
def render_dataframe(df, title: str | None = None): ...
def render_dataframe_download(df, filename: str): ...
```

要求：

1. 自动处理 `None` 和空 DataFrame。
2. CSV 使用 `utf-8-sig` 编码，方便 Excel 打开中文。
3. 表格默认 `use_container_width=True`。

### 16.3 metrics.py

新增：`src/quant_fund_lab/ui/components/metrics.py`

至少提供：

```python
def render_metric_cards(metrics: dict): ...
```

### 16.4 logs.py

新增：`src/quant_fund_lab/ui/components/logs.py`

至少提供：

```python
def render_service_result(result: ServiceResult, show_detail: bool = False): ...
```

要求：

1. success=True 显示成功信息。
2. success=False 显示错误信息。
3. error_detail 只在展开区域显示。

---

## 17. Streamlit 启动器

新增：`src/quant_fund_lab/ui/launcher.py`

```python
from __future__ import annotations

from pathlib import Path
import subprocess
import sys


def main() -> None:
    app_path = Path(__file__).resolve().parent / "streamlit_app.py"
    subprocess.run(
        [sys.executable, "-m", "streamlit", "run", str(app_path)],
        check=True,
    )
```

在 `pyproject.toml` 的 `[project.scripts]` 增加：

```toml
qfl-ui = "quant_fund_lab.ui.launcher:main"
```

说明：这里允许 `launcher.py` 使用 `subprocess` 启动 Streamlit；但 UI 页面本身不要用 `subprocess` 调旧 CLI 命令。

---

## 18. README 更新要求

README 中新增：

```markdown
## 图形界面使用方式

项目推荐使用本地浏览器 UI：

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
```

同时保留当前“常用命令”，但把它放到“开发者命令”小节。

---

## 19. 测试要求

新增测试：

```text
tests/test_ui_services.py
tests/test_ui_report_service.py
tests/test_ui_market_data_service.py
```

至少覆盖：

1. `ServiceResult` 结构。
2. 数据中心 service 在演示数据模式下能返回成功。
3. 报告 service 在 reports 不存在时不崩溃。
4. signal service 在缺少 price matrix 时返回友好错误。
5. rotation service 在缺少 price matrix 时返回友好错误。
6. market backtest service 能运行 MA Cross 演示回测。

不要对 Streamlit 页面做重型端到端测试，优先测 service 层。

---

## 20. 非破坏性重构要求

Codex 必须遵守：

1. 不删除当前 CLI。
2. 不改坏当前 `qfl-data`、`qfl-demo-data`、`qfl-backtest`、`qfl-signal`、`qfl-market-demo`。
3. 不把 UI 页面写成一堆重复业务逻辑。
4. 不把 API token、私有路径、用户本机绝对路径写死进代码。
5. 不在 UI 页面中长期使用 `subprocess.run(["uv", "run", "qfl-..."])` 调用旧命令。
6. 可以对旧函数做“增加参数、增加返回值、抽取公共函数”的兼容性改造。
7. 每改一个旧入口，都要保证原命令仍能运行。

---

## 21. 建议执行顺序

### Phase 1：新增 UI 骨架

1. `uv add streamlit`
2. 新增 `src/quant_fund_lab/ui/streamlit_app.py`
3. 新增 `src/quant_fund_lab/ui/pages/`
4. 新增 `qfl-ui` 脚本入口
5. 验证：`uv run qfl-ui` 能打开首页

### Phase 2：封装公共组件

1. `ServiceResult`
2. `task_runner`
3. `tables.py`
4. `charts.py`
5. `logs.py`
6. `metrics.py`

### Phase 3：迁移数据中心

1. 接入 demo 数据生成
2. 接入 AKShare 数据下载
3. 接入 Parquet 预览
4. 完成数据中心页面

### Phase 4：迁移轮动策略和信号

1. 封装 rotation service
2. 封装 signal service
3. 完成轮动回测页面
4. 完成模拟信号页面

### Phase 5：迁移 market 看盘与轻量回测

1. 接入 `market.services.data_service`
2. 做 K 线/指标展示
3. 接入 `market.services.backtest_service`
4. 展示轻量回测指标、订单和权益曲线

### Phase 6：报告中心、诊断、README、测试

1. 报告中心
2. 设置诊断
3. README 更新
4. service 层测试
5. 运行 `uv run pytest`

---

## 22. 最小可交付版本

第一轮 PR 至少完成：

1. `uv run qfl-ui` 可启动。
2. 首页可见。
3. 数据中心可生成演示数据并预览 `etf_close.parquet`。
4. 轮动回测页面可运行 demo 数据上的回测并展示 `result.stats`。
5. 模拟信号页面可生成 `latest_signal.csv`。
6. README 有 UI 使用说明。
7. 旧 CLI 不受影响。

第二轮 PR 完成：

1. 看盘中心。
2. 技术指标展示。
3. 轻量策略回测页面。
4. 报告中心。
5. 设置诊断。
6. 更完整的 service 测试。

---

## 23. 最终验收清单

```markdown
- [ ] 新增 `qfl-ui` 启动命令。
- [ ] `uv run qfl-ui` 能启动 Streamlit UI。
- [ ] 数据中心替代 `qfl-data` 和 `qfl-demo-data`。
- [ ] 轮动回测替代 `qfl-backtest`。
- [ ] 模拟信号替代 `qfl-signal`。
- [ ] 策略回测替代 `qfl-market-demo`。
- [ ] 看盘中心可拉取并展示单标的行情。
- [ ] 指标 MA、RSI、MACD、Bollinger 可视化展示。
- [ ] 报告中心可预览和下载 reports 文件。
- [ ] 设置诊断页可显示依赖、路径、数据状态。
- [ ] README 已更新。
- [ ] 新增 service 层测试。
- [ ] `uv run pytest` 通过。
- [ ] 旧 CLI 命令仍可运行。
```

---

## 24. 给 Codex 的最终指令

请在当前仓库中新增本地浏览器 UI，不要移除原 CLI。优先把当前已经存在的命令行能力迁移到 Streamlit 页面中，并通过 service 层复用现有函数。

开发时请严格遵循：

1. UI 文件放到 `src/quant_fund_lab/ui/`。
2. 新增 `qfl-ui` 作为主入口。
3. 页面不要直接堆业务逻辑。
4. 每个旧 CLI 功能都要有对应 UI 页面。
5. 所有结果都要能在页面中看到，而不是只在终端中打印。
6. 所有表格结果都要支持 CSV 下载。
7. 所有错误都要显示友好提示。
8. 更新 README 和测试。

交付时请在回复中列出：

1. 修改文件清单。
2. 旧 CLI 到 UI 页面的映射表。
3. 启动方式。
4. 测试命令和结果。
5. 尚未迁移的功能，如有。
