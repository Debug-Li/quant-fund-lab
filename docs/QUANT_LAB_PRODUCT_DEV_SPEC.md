# 量观 Quant Lab 本地量化平台产品与开发规格文档

> 文件建议路径：`docs/QUANT_LAB_PRODUCT_DEV_SPEC.md`  
> 执行对象：Codex  
> 目标：开发一个与产品图 UI 和功能逻辑保持一致的本地量化研究平台。  
> 约束：不强制沿用现有 UI 或架构；可以在保留已有量化能力的基础上重构，也可以新建前后端架构。最终效果以本文档定义的页面、视觉和交互为准。

---

## 1. 产品定位

产品名称：

```text
量观 Quant Lab
```

产品定位：

```text
本地运行的专业量化研究、看盘、回测、组合管理与风险监控平台。
```

用户打开平台后，应看到一个接近专业金融终端的深色高可视化界面，而不是传统命令行工具或简单表单页面。

核心目标：

1. 所有主要功能通过图形界面完成。
2. 页面视觉与产品图保持一致：深色金融终端风格、高信息密度、多图表、多指标、多面板。
3. 支持本地数据、本地回测、本地策略研究。
4. 可接入真实数据，也必须内置 demo 数据，保证无网络或无数据时页面仍可完整展示。
5. 不以实盘交易为第一目标，第一阶段聚焦研究、回测、信号、组合和风控。
6. 所有策略、回测、数据下载、信号生成、报告查看都应从 UI 中完成，不要求用户手动执行命令行。

---

## 2. 最终交付形态

建议交付为本地 Web 应用：

```text
用户启动本地服务 -> 浏览器打开 http://localhost:xxxx -> 使用量观 Quant Lab
```

启动命令建议：

```bash
uv run quant-lab
```

或：

```bash
uv run qfl-ui
```

如果项目不使用 uv，也可以支持：

```bash
python -m quant_lab
```

---

## 3. 推荐技术架构

### 3.1 推荐方案：React + FastAPI + Python Quant Engine

为了尽可能还原产品图的复杂布局和交互，推荐采用前后端分离架构：

```text
Frontend:
  React
  Vite
  TypeScript
  ECharts
  Plotly.js，可选
  TanStack Table
  Zustand 或 Redux Toolkit
  Tailwind CSS 或 CSS Modules

Backend:
  FastAPI
  Pydantic
  pandas
  numpy
  duckdb / sqlite / parquet
  APScheduler，可选
  existing quant engine / backtest engine

Quant Core:
  data providers
  indicator engine
  strategy engine
  backtest engine
  portfolio engine
  risk engine
  report engine
```

### 3.2 为什么不用简单 Streamlit 作为最终目标

Streamlit 适合快速验证，但产品图中有以下要求：

1. 固定左侧导航和顶部工具栏。
2. 复杂多面板金融终端布局。
3. 高密度卡片和图表。
4. K 线、盘口、热力图、矩阵、雷达图、时间线联动。
5. 更强的交互体验：点击自选股切换主图、拖拽布局、图表联动、策略参数动态表单。

这些更适合 React + ECharts / Plotly 实现。

### 3.3 允许复用现有代码

如果当前仓库已有 Python 数据、回测、策略、信号、报告逻辑，Codex 应优先复用。

原则：

1. 业务逻辑保留在 Python 后端。
2. 前端只负责展示、交互和参数输入。
3. 不要在前端实现核心回测算法。
4. CLI 可以保留，但普通用户主入口必须是 UI。

---

## 4. 建议项目结构

如果从当前仓库改造，建议增加如下结构：

```text
quant-fund-lab/
  apps/
    web/
      package.json
      index.html
      vite.config.ts
      tsconfig.json
      src/
        main.tsx
        App.tsx
        routes/
          DashboardPage.tsx
          MarketWatchPage.tsx
          StrategyLabPage.tsx
          BacktestPage.tsx
          PortfolioPage.tsx
          SignalCenterPage.tsx
          DataCenterPage.tsx
          RiskMonitorPage.tsx
          ReportsPage.tsx
          SettingsPage.tsx
        components/
          shell/
            AppShell.tsx
            SideNav.tsx
            TopBar.tsx
            PageHeader.tsx
          cards/
            MetricCard.tsx
            RiskCard.tsx
            StatusCard.tsx
          charts/
            EquityCurveChart.tsx
            CandlestickChart.tsx
            VolumeChart.tsx
            MacdChart.tsx
            RsiChart.tsx
            DonutAllocationChart.tsx
            MarketHeatmap.tsx
            RiskBars.tsx
            ParamHeatmap.tsx
            MonthlyReturnHeatmap.tsx
            ReturnDistributionChart.tsx
            RollingMetricsChart.tsx
            FactorRadarChart.tsx
            CorrelationHeatmap.tsx
            TreemapChart.tsx
            WaterfallChart.tsx
            CapitalFlowChart.tsx
          tables/
            TradesTable.tsx
            HoldingsTable.tsx
            WatchlistTable.tsx
            SignalTable.tsx
            ReportsTable.tsx
          timeline/
            SignalTimeline.tsx
            NewsTimeline.tsx
            LogTimeline.tsx
          controls/
            MarketTabs.tsx
            DateRangePicker.tsx
            SymbolSearch.tsx
            StrategySelector.tsx
            ParameterGrid.tsx
          layout/
            Panel.tsx
            SplitGrid.tsx
            RightSidebar.tsx
          ui/
            Badge.tsx
            Button.tsx
            Select.tsx
            Input.tsx
            Tabs.tsx
            Tooltip.tsx
        services/
          api.ts
          dashboardApi.ts
          marketApi.ts
          strategyApi.ts
          backtestApi.ts
          portfolioApi.ts
          signalApi.ts
          dataApi.ts
          riskApi.ts
          reportApi.ts
        store/
          appStore.ts
          marketStore.ts
          backtestStore.ts
        theme/
          tokens.ts
          global.css
        types/
          dashboard.ts
          market.ts
          strategy.ts
          backtest.ts
          portfolio.ts
          signal.ts
          risk.ts
          report.ts

  src/
    quant_lab/
      api/
        main.py
        deps.py
        routers/
          dashboard.py
          market.py
          strategy.py
          backtest.py
          portfolio.py
          signal.py
          data.py
          risk.py
          report.py
          settings.py
      core/
        config.py
        paths.py
        logging.py
      data/
        providers/
        storage/
      indicators/
      strategies/
      backtest/
      portfolio/
      risk/
      reports/
      services/
        dashboard_service.py
        market_service.py
        strategy_service.py
        backtest_service.py
        portfolio_service.py
        signal_service.py
        data_service.py
        risk_service.py
        report_service.py
        demo_data_service.py
      schemas/
        dashboard.py
        market.py
        strategy.py
        backtest.py
        portfolio.py
        signal.py
        risk.py
        report.py

  data/
    raw/
    processed/
    local/
    demo/

  reports/
    backtests/
    signals/
    risk/
    exports/

  docs/
    QUANT_LAB_PRODUCT_DEV_SPEC.md
```

如果当前项目已经有 `src/quant_fund_lab` 命名，Codex 可以继续使用该包名，不必强行改成 `quant_lab`。关键是架构分层必须清晰。

---

## 5. 视觉设计规范

### 5.1 总体风格

产品图风格关键词：

```text
深色金融终端
高信息密度
卡片化面板
蓝色主色
红绿涨跌
大量图表
中文专业界面
桌面端宽屏
```

### 5.2 颜色系统

前端建立统一主题变量：

```ts
export const theme = {
  colors: {
    bg: "#06101f",
    bgElevated: "#0a1728",
    panel: "#0d1b2e",
    panelSoft: "#10243a",
    panelHover: "#132c49",
    border: "#1f3857",
    borderSoft: "rgba(90, 140, 200, 0.22)",

    text: "#e6eef8",
    textMuted: "#8ea3bd",
    textSubtle: "#5f7898",

    primary: "#1677ff",
    primaryHover: "#2f9bff",
    cyan: "#13c2c2",
    purple: "#9254de",

    positive: "#00c781",
    positiveSoft: "rgba(0, 199, 129, 0.16)",
    negative: "#ff4d4f",
    negativeSoft: "rgba(255, 77, 79, 0.16)",
    warning: "#faad14",
    warningSoft: "rgba(250, 173, 20, 0.16)",

    grid: "rgba(140, 170, 210, 0.12)",
  }
}
```

### 5.3 字体

建议：

```css
font-family:
  Inter,
  "SF Pro Display",
  "PingFang SC",
  "Microsoft YaHei",
  system-ui,
  sans-serif;
```

数字建议：

```css
font-variant-numeric: tabular-nums;
```

### 5.4 页面宽度

目标桌面端：

```text
最低支持：1366 × 768
推荐尺寸：1680 × 945
最佳尺寸：1920 × 1080
```

不以移动端为第一优先级。移动端可以只保证不崩溃，不要求完整体验。

### 5.5 左侧导航

固定左侧导航栏宽度：

```text
展开：220px
收起：64px
```

导航项：

```text
总览
市场看盘
策略研究
回测分析
组合管理
信号中心
数据中心
风险监控
报告中心
设置
```

每个导航项有图标、中文标题、选中高亮。

### 5.6 顶部工具栏

顶部工具栏高度：

```text
56px ~ 64px
```

包含：

1. 产品 Logo：量观 Quant Lab。
2. 搜索框：搜索标的 / 策略 / 指标 / 资讯。
3. 市场切换：美股 / A股 / ETF / 期货。
4. 周期切换：日线 / 60m / 15m / 5m。
5. 日期范围。
6. 数据刷新。
7. 运行回测。
8. 用户头像 / 本地运行状态。

### 5.7 面板规范

所有模块使用卡片面板：

```css
background: linear-gradient(180deg, #0d1b2e 0%, #0a1728 100%);
border: 1px solid rgba(90, 140, 200, 0.22);
border-radius: 12px;
box-shadow: 0 10px 30px rgba(0, 0, 0, 0.18);
```

### 5.8 数据颜色

```text
上涨 / 收益 / 正贡献：绿色
下跌 / 亏损 / 风险：红色
中性：蓝灰色
提示：蓝色
警告：橙色
严重告警：红色
```

---

## 6. 数据和后端 API 设计

### 6.1 API 基础路径

```text
/api/dashboard
/api/market
/api/strategy
/api/backtest
/api/portfolio
/api/signal
/api/data
/api/risk
/api/report
/api/settings
```

### 6.2 通用响应格式

```python
class ApiResponse(BaseModel):
    success: bool
    message: str = ""
    data: Any | None = None
    error: str | None = None
    logs: list[str] = []
```

错误不直接返回大段 traceback。开发环境可以在 `debug` 字段中返回详细信息。

---

## 7. Demo 数据要求

必须实现 demo 数据服务，保证前端在没有真实数据时仍能完整渲染。

后端文件：

```text
src/quant_lab/services/demo_data_service.py
```

必须提供：

```python
get_demo_dashboard()
get_demo_market_watch(symbol: str = "NVDA")
get_demo_backtest()
get_demo_portfolio()
get_demo_signals()
get_demo_risk()
get_demo_reports()
```

要求：

1. 数据看起来真实，但标注为演示数据。
2. 日期、价格、收益、回撤、持仓、盘口、新闻等字段完整。
3. 图表不能因为空数据而崩溃。
4. 测试不能依赖真实网络。

---

## 8. 页面一：总览 Dashboard

### 8.1 视觉目标

总览页对应产品图第一张：打开平台后的主仪表盘。

它必须像一个专业金融终端首页，包含组合、市场、风险、信号和任务日志的全局视图。

### 8.2 页面布局

```text
左侧导航
顶部工具栏
中央主内容 3 列布局
右侧信息栏
```

建议 Grid：

```text
主内容宽度：约 75%
右侧栏宽度：约 25%
```

中央区域：

1. 顶部 KPI 卡片行。
2. 组合净值曲线。
3. 资产配置环形图。
4. 市场热力图。
5. 风险指标面板。
6. 最近交易记录。
7. 信号提醒。

右侧栏：

1. 今日市场情绪仪表。
2. 资金流向面积图。
3. 运行日志摘要。

### 8.3 KPI 卡片

五张卡片：

```text
总资产
今日收益
累计收益率
最大回撤
夏普比率
```

字段：

```ts
type KpiCard = {
  title: string
  value: string | number
  unit?: string
  delta?: number
  deltaLabel?: string
  sparkline?: Array<{ time: string; value: number }>
  status: "positive" | "negative" | "neutral"
}
```

### 8.4 组合净值曲线

图表：

```text
组合净值 vs 基准
```

功能：

1. 支持近1月、近3月、近6月、近1年、全部。
2. Hover 显示日期、组合净值、基准净值。
3. 右上角显示当前净值和基准。
4. 可叠加回撤，可选。

### 8.5 资产配置

环形图分类：

```text
股票
ETF
现金
期货
其他
```

显示：

1. 占比。
2. 金额。
3. 中心显示总资产。

### 8.6 市场热力图

行业块：

```text
科技
半导体
软件
金融
医疗保健
消费电子
工业
通信服务
能源
房地产
材料
公用事业
```

颜色：

```text
绿色：上涨
红色：下跌
颜色深浅：涨跌幅绝对值
```

### 8.7 风险指标面板

指标：

```text
年化波动率
Beta
Alpha
最大回撤
胜率
换手率
```

每个指标用横向条形或仪表表示，显示当前值和阈值。

### 8.8 最近交易记录

字段：

```text
时间
标的
方向
成交价
数量
收益
收益率
```

### 8.9 信号提醒

类型：

```text
买入信号
卖出信号
风控提醒
数据更新
回测完成
```

显示为时间线。

### 8.10 API

```text
GET /api/dashboard/overview
```

返回：

```ts
type DashboardOverview = {
  demo: boolean
  kpis: KpiCard[]
  equityCurve: EquityPoint[]
  allocation: AllocationItem[]
  marketHeatmap: HeatmapItem[]
  riskMetrics: RiskMetric[]
  recentTrades: TradeRow[]
  signals: SignalRow[]
  marketSentiment: MarketSentiment
  capitalFlow: TimeSeriesPoint[]
  logs: LogRow[]
}
```

---

## 9. 页面二：市场看盘 Market Watch

### 9.1 视觉目标

对应产品图“市场看盘”页：左侧主 K 线，右侧盘口和自选股，下方多标的对比、板块资金流、新闻和信号。

### 9.2 页面模块

1. 标的基础信息。
2. K 线主图。
3. 成交量。
4. MACD。
5. RSI。
6. 盘口 / Level 2。
7. 自选股。
8. 多标的对比。
9. 板块资金流向。
10. AI 市场摘要。
11. 新闻/事件/财报时间线。
12. 信号提醒。
13. 策略运行状态。

### 9.3 顶部控件

```text
标的搜索
市场切换
周期：日线 / 60m / 15m / 5m
日期范围
指标选择
刷新数据
运行回测
```

### 9.4 K 线图

必须实现：

1. 蜡烛图。
2. MA5、MA20、MA60。
3. 成交量。
4. MACD。
5. RSI。
6. 最新价标注。
7. 前复权 / 后复权 / 不复权选项。
8. Hover 联动。

推荐 ECharts：

```ts
CandlestickChart.tsx
VolumeChart.tsx
MacdChart.tsx
RsiChart.tsx
```

### 9.5 盘口面板

第一阶段允许模拟 Level 2：

字段：

```text
卖五、卖四、卖三、卖二、卖一
买一、买二、买三、买四、买五
价格
数量
买卖盘比例
分时成交
```

面板必须标注：

```text
模拟盘口，仅供研究
```

如果未来接入真实数据，再移除提示。

### 9.6 自选股

字段：

```text
代码
名称
迷你走势
最新价
涨跌幅
成交额
```

交互：

1. 点击自选股，切换主 K 线标的。
2. 星标收藏。
3. 增加自选。
4. 删除自选。
5. 本地持久化到配置文件或数据库。

### 9.7 多标的对比

支持同时显示：

```text
NVDA
AAPL
SPY
QQQ
```

用户可添加和删除对比标的。

### 9.8 板块资金流

展示：

1. 板块热力图。
2. 净流入金额。
3. 涨跌幅。
4. 排行榜。

### 9.9 AI 市场摘要

第一阶段不需要真实大模型，可以用规则模板生成摘要。

示例：

```text
今日美股三大指数涨跌不一。半导体与 AI 板块资金流入居前，NVDA 突破近期高位，短期动能增强。风险提示：关注利率波动与大盘回撤。
```

### 9.10 API

```text
GET /api/market/snapshot?symbol=NVDA&market=US&period=1d
GET /api/market/watchlist
POST /api/market/watchlist
DELETE /api/market/watchlist/{symbol}
GET /api/market/sector-flow
GET /api/market/news
```

---

## 10. 页面三：策略研究 Strategy Lab

### 10.1 视觉目标

策略研究页用于管理策略文件、查看代码、编辑参数、查看策略说明，并可快速运行回测。

### 10.2 页面模块

1. 策略列表。
2. 策略代码编辑器。
3. 参数表单。
4. 策略说明。
5. 策略模板库。
6. 最近运行记录。
7. 快速运行按钮。

### 10.3 策略编辑器

前端可使用：

```text
Monaco Editor
```

如果不想引入 Monaco，第一阶段可用只读代码块 + 参数表单。

功能：

1. 查看策略代码。
2. 新建策略。
3. 复制策略。
4. 保存策略。
5. 参数 schema 自动生成表单。

安全要求：

1. 禁止路径穿越。
2. 只允许保存到项目策略目录。
3. 运行前必须显示风险提示。
4. 后端执行策略时必须限制工作目录。

### 10.4 策略配置 schema

```yaml
name: MA 动量轮动策略
description: 基于双均线动量进行月度调仓
file: ma_rotation.py
params:
  fast_window:
    type: int
    label: 快线周期
    default: 20
    min: 5
    max: 60
    step: 5
  slow_window:
    type: int
    label: 慢线周期
    default: 60
    min: 20
    max: 240
    step: 10
  stop_loss:
    type: float
    label: 止损比例
    default: 0.08
    min: 0.02
    max: 0.20
    step: 0.01
```

### 10.5 API

```text
GET /api/strategy/list
GET /api/strategy/{strategy_id}
POST /api/strategy
PUT /api/strategy/{strategy_id}
POST /api/strategy/{strategy_id}/validate
```

---

## 11. 页面四：回测分析 Backtest

### 11.1 视觉目标

对应产品图“回测分析”：左侧策略代码和参数，中间净值、回撤和指标，右侧日志、策略说明和风险提示。

### 11.2 顶部控件

```text
策略选择
标的池
基准
回测区间
初始资金
手续费
滑点
运行回测
保存策略
导出报告
```

### 11.3 KPI

```text
总收益率
年化收益
最大回撤
夏普比率
胜率
Calmar
```

### 11.4 主图

```text
策略净值曲线 vs 基准净值
回撤面积图
```

### 11.5 分析图表

1. 参数寻优热力图。
2. 月度收益热力图。
3. 收益分布直方图。
4. 滚动收益 / 滚动波动率。
5. 交易明细表。

### 11.6 参数寻优

第一阶段支持二维参数热力图：

```text
X 轴：快线周期
Y 轴：慢线周期
值：夏普比率 / 年化收益 / 最大回撤
```

### 11.7 交易明细表

字段：

```text
开仓时间
平仓时间
标的
方向
开仓价格
平仓价格
持仓天数
收益率
收益金额
仓位
交易类型
```

### 11.8 运行日志

右侧时间线：

```text
开始初始化回测环境
加载标的池数据
加载历史行情数据
生成策略信号
执行交易撮合
计算权益曲线
计算绩效指标
生成分析图表
回测完成
```

### 11.9 API

```text
POST /api/backtest/run
POST /api/backtest/optimize
GET /api/backtest/result/{backtest_id}
GET /api/backtest/history
GET /api/backtest/report/{backtest_id}
```

---

## 12. 页面五：组合管理 Portfolio

### 12.1 视觉目标

对应产品图“组合管理 / 风险监控”：展示组合市值、收益、风险、持仓、因子、相关性、再平衡建议。

### 12.2 顶部控件

```text
组合选择
策略组合
基准
日期范围
再平衡
风险检测
```

### 12.3 KPI

```text
组合市值
日收益
累计收益
VaR(95%)
CVaR(95%)
最大回撤
杠杆率
```

### 12.4 图表

1. 组合净值与回撤。
2. 资产配置环形图。
3. 持仓明细表。
4. 因子暴露雷达图。
5. 相关性矩阵热力图。
6. 行业/主题权重 treemap。
7. 风险贡献瀑布图。
8. 风控告警中心。
9. 调仓建议。
10. 再平衡建议。

### 12.5 持仓明细字段

```text
标的
名称
行业
权重
成本价
现价
市值
盈亏
贡献度
```

### 12.6 调仓建议规则

第一阶段使用规则引擎：

1. 单标的权重 > 15%：建议减持。
2. 行业权重 > 30%：建议降低集中度。
3. 持仓相关性均值 > 0.75：建议分散。
4. 当前回撤 > 8%：建议降低仓位。
5. 现金占比 < 3%：提示流动性风险。
6. Beta > 1.2：建议降低市场暴露。

### 12.7 API

```text
GET /api/portfolio/overview
GET /api/portfolio/holdings
GET /api/portfolio/risk
POST /api/portfolio/rebalance/simulate
GET /api/portfolio/rebalance/suggestion
```

---

## 13. 页面六：信号中心 Signal Center

### 13.1 页面目标

集中展示策略信号、风控信号、调仓信号和数据更新状态。

### 13.2 模块

1. 今日信号概览。
2. 买入信号。
3. 卖出信号。
4. 风控提醒。
5. 调仓建议。
6. 历史信号表。
7. 信号详情抽屉。

### 13.3 信号字段

```text
时间
类型
标的
名称
当前价
信号强度
来源策略
建议动作
状态
备注
```

### 13.4 API

```text
GET /api/signal/list
POST /api/signal/generate
POST /api/signal/{signal_id}/confirm
POST /api/signal/{signal_id}/ignore
```

---

## 14. 页面七：数据中心 Data Center

### 14.1 页面目标

替代命令行数据下载、检查和导出。

### 14.2 模块

1. 数据源状态。
2. 本地数据概览。
3. 下载行情数据。
4. 生成演示数据。
5. 数据质量检查。
6. 数据预览。
7. 数据导出。
8. 缓存清理。

### 14.3 数据质量检查

检查项：

1. 缺失值。
2. 重复日期。
3. 价格为 0。
4. 异常涨跌幅。
5. 数据起止日期。
6. 标的数量。
7. 文件大小。
8. 更新时间。

### 14.4 API

```text
GET /api/data/status
POST /api/data/download
POST /api/data/demo
GET /api/data/preview
POST /api/data/quality-check
POST /api/data/export
DELETE /api/data/cache
```

---

## 15. 页面八：风险监控 Risk Monitor

### 15.1 页面目标

独立展示风险状态，强调回撤、波动、VaR、CVaR、集中度、流动性和告警。

### 15.2 风险指标

```text
最大回撤
当前回撤
年化波动率
VaR(95%)
CVaR(95%)
Beta
Alpha
胜率
盈亏比
集中度
换手率
流动性风险
```

### 15.3 告警规则

```text
当前回撤 > 8%：中风险
当前回撤 > 12%：高风险
单一标的权重 > 15%：集中度风险
行业权重 > 30%：行业集中风险
年化波动率 > 25%：波动风险
相关性均值 > 0.75：相关性过高
现金占比 < 3%：流动性不足
```

### 15.4 可视化

1. 风险 KPI 卡片。
2. 回撤曲线。
3. VaR / CVaR 分布图。
4. 相关性矩阵。
5. 风险贡献图。
6. 告警时间线。
7. AI 风险摘要。

### 15.5 API

```text
GET /api/risk/overview
GET /api/risk/alerts
POST /api/risk/check
GET /api/risk/report
```

---

## 16. 页面九：报告中心 Reports

### 16.1 页面目标

集中查看回测、信号、风险和数据导出的产物。

### 16.2 功能

1. 报告列表。
2. 类型筛选。
3. 时间筛选。
4. CSV 预览。
5. 图片预览。
6. HTML 报告预览。
7. 下载文件。
8. 删除文件。

### 16.3 API

```text
GET /api/report/list
GET /api/report/{report_id}
GET /api/report/{report_id}/download
DELETE /api/report/{report_id}
```

---

## 17. 页面十：设置 Settings

### 17.1 功能

1. 项目根目录。
2. 数据目录。
3. 报告目录。
4. 默认市场。
5. 默认标的。
6. 默认基准。
7. 数据源优先级。
8. API Token 配置状态。
9. Python 版本。
10. 前端版本。
11. 后端版本。
12. 依赖检查。
13. 日志级别。
14. 主题设置，可选。

### 17.2 安全要求

1. 不显示完整 token。
2. 不把 token 写入 Git。
3. 只显示“已配置 / 未配置”。
4. 本地配置文件应加入 `.gitignore`。

### 17.3 API

```text
GET /api/settings
PUT /api/settings
GET /api/settings/diagnostics
```

---

## 18. 核心业务逻辑模块

### 18.1 数据模块

功能：

1. 获取历史 OHLCV。
2. 获取 ETF / 股票 / 指数数据。
3. 本地缓存。
4. 数据质量检查。
5. 数据复权处理。
6. 数据导出。

### 18.2 指标模块

必须实现：

```text
MA
EMA
MACD
RSI
Bollinger Bands
ATR
收益率
累计收益
回撤
波动率
```

### 18.3 回测模块

支持：

1. 单标的回测。
2. 多标的轮动回测。
3. 手续费。
4. 滑点。
5. 初始资金。
6. 调仓频率。
7. 止损。
8. 交易记录。
9. 资金曲线。
10. 回撤曲线。
11. 指标计算。

### 18.4 组合模块

支持：

1. 持仓统计。
2. 资产配置。
3. 行业权重。
4. 收益贡献。
5. 风险贡献。
6. 相关性矩阵。
7. 因子暴露。
8. 再平衡模拟。

### 18.5 风险模块

支持：

1. 最大回撤。
2. 当前回撤。
3. 年化波动率。
4. VaR。
5. CVaR。
6. Beta。
7. Alpha。
8. 集中度。
9. 流动性。
10. 相关性。
11. 告警规则。

---

## 19. 前端组件验收要求

### 19.1 必须实现的通用组件

```text
AppShell
SideNav
TopBar
Panel
MetricCard
StatusBadge
TrendNumber
DataTable
DownloadButton
SignalTimeline
LogTimeline
RiskAlertList
```

### 19.2 必须实现的图表组件

```text
EquityCurveChart
CandlestickChart
VolumeChart
MacdChart
RsiChart
DonutAllocationChart
MarketHeatmap
CapitalFlowChart
RiskBars
ParamHeatmap
MonthlyReturnHeatmap
ReturnDistributionChart
RollingMetricsChart
FactorRadarChart
CorrelationHeatmap
TreemapChart
WaterfallChart
```

---

## 20. 开发阶段

### Phase 0：项目初始化与技术选型确认

Codex 先检查当前仓库。

如果已有可复用 Python 量化逻辑：

1. 保留已有逻辑。
2. 新增 FastAPI 包装层。
3. 新增 React 前端。

如果现有 UI 不满足产品图：

1. 可以保留旧 UI 作为 legacy。
2. 新 UI 以 `apps/web` 为主。
3. 最终启动命令指向新 UI。

### Phase 1：后端 API 骨架

1. 创建 FastAPI app。
2. 创建路由模块。
3. 创建 demo data service。
4. 所有页面 API 先返回 demo 数据。
5. 加入 CORS。
6. 加入统一错误处理。

验收：

```text
GET /api/health 返回 ok
GET /api/dashboard/overview 返回完整 demo JSON
```

### Phase 2：前端基础框架

1. 创建 React + Vite + TypeScript 项目。
2. 建立深色主题。
3. 实现 AppShell、SideNav、TopBar。
4. 建立路由。
5. 实现 API client。
6. 实现基础 Panel 和 MetricCard。

验收：

```text
前端可启动
左侧导航和顶部工具栏与产品图一致
可以切换页面
```

### Phase 3：总览页

1. KPI 卡片。
2. 组合净值曲线。
3. 资产配置环形图。
4. 市场热力图。
5. 风险指标。
6. 交易记录。
7. 信号时间线。
8. 市场情绪和资金流。

验收：

```text
总览页视觉接近产品图第一张
```

### Phase 4：市场看盘页

1. K 线。
2. 成交量。
3. MA。
4. MACD。
5. RSI。
6. 盘口。
7. 自选股。
8. 多标的对比。
9. 板块资金流。
10. 新闻和信号。

验收：

```text
市场看盘页视觉接近产品图市场看盘页
```

### Phase 5：回测分析页

1. 策略选择。
2. 参数配置。
3. KPI。
4. 净值和回撤。
5. 参数热力图。
6. 月度收益热力图。
7. 收益分布。
8. 交易明细。
9. 运行日志。

验收：

```text
回测分析页视觉接近产品图回测页
```

### Phase 6：组合管理与风险监控

1. 组合 KPI。
2. 资产配置。
3. 持仓明细。
4. 因子雷达图。
5. 相关性矩阵。
6. 风险贡献。
7. 调仓建议。
8. 风险告警。

验收：

```text
组合管理页视觉接近产品图组合风控页
```

### Phase 7：接入真实业务逻辑

将 demo API 逐步替换为真实服务：

1. 数据中心接入真实数据下载。
2. 市场看盘接入本地或在线行情。
3. 回测页接入真实回测引擎。
4. 信号中心接入真实信号生成。
5. 报告中心接入真实报告文件。
6. 风险监控接入真实组合风险计算。

要求：

```text
真实数据失败时 fallback 到 demo 数据，并显示提示。
```

### Phase 8：测试、文档与交付

1. 后端 pytest。
2. 前端组件测试，可选。
3. API schema 测试。
4. README 更新。
5. 启动文档。
6. 截图或录屏说明。

---

## 21. 测试要求

### 21.1 后端测试

```text
test_health_api.py
test_dashboard_api.py
test_market_api.py
test_backtest_api.py
test_portfolio_api.py
test_risk_api.py
test_demo_data_service.py
test_indicators.py
test_backtest_engine.py
test_risk_rules.py
```

### 21.2 前端测试

最低要求：

1. AppShell 渲染。
2. 路由切换。
3. MetricCard 渲染。
4. 图表组件空数据不崩溃。
5. API 失败时显示错误态。

### 21.3 不允许

1. 测试依赖真实网络。
2. 测试依赖当天行情。
3. 空数据导致页面崩溃。
4. API 错误直接白屏。

---

## 22. README 更新要求

README 必须新增：

```markdown
## 启动量观 Quant Lab

### 后端

```bash
uv run quant-lab-api
```

### 前端

```bash
cd apps/web
npm install
npm run dev
```

### 一键启动，可选

```bash
uv run quant-lab
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
```

---

## 23. 最终验收清单

Codex 交付前必须逐项确认：

```markdown
- [ ] 新 UI 不再是简单 Streamlit 表单，而是接近产品图的金融终端界面。
- [ ] 左侧导航和顶部工具栏与产品图一致。
- [ ] 总览页完成。
- [ ] 市场看盘页完成。
- [ ] 策略研究页完成。
- [ ] 回测分析页完成。
- [ ] 组合管理页完成。
- [ ] 信号中心页完成。
- [ ] 数据中心页完成。
- [ ] 风险监控页完成。
- [ ] 报告中心页完成。
- [ ] 设置页完成。
- [ ] K 线、成交量、MACD、RSI 可显示。
- [ ] 净值曲线、回撤曲线、资产配置、热力图可显示。
- [ ] 参数寻优热力图、月度收益热力图、收益分布图可显示。
- [ ] 因子雷达图、相关性矩阵、风险贡献图可显示。
- [ ] 所有页面无真实数据时能用 demo 数据完整展示。
- [ ] 后端 API 有统一响应格式。
- [ ] 前端 API 错误有友好提示。
- [ ] 不硬编码 API token。
- [ ] 不删除已有量化核心逻辑，除非用户允许。
- [ ] README 已更新。
- [ ] 后端测试通过。
- [ ] 前端可以正常启动。
```

---

## 24. 禁止事项

Codex 不要做以下事情：

1. 不要把最终 UI 做成简单表单页面。
2. 不要为了省事只保留命令行入口。
3. 不要只做 Streamlit 默认样式，必须按产品图风格做高保真 UI。
4. 不要把量化算法写在前端。
5. 不要让页面依赖真实网络才能显示。
6. 不要直接暴露 traceback 给用户。
7. 不要硬编码 token、密钥、账号。
8. 不要默认接入真实交易下单。
9. 不要删除旧核心逻辑，除非确认无法复用。
10. 不要把 demo 数据伪装为真实行情。

---

## 25. 给 Codex 的最终指令

请根据本文档开发“量观 Quant Lab”本地量化平台。你可以基于现有仓库重构，也可以新增 React + FastAPI 架构。最终标准不是保留现有 UI，而是让开发后的 UI 和逻辑与产品图保持一致。

优先顺序：

1. 先搭建 FastAPI + demo data API。
2. 再搭建 React/Vite/TypeScript 前端壳。
3. 实现总览、市场看盘、回测分析、组合管理四个核心页面。
4. 再补策略研究、信号中心、数据中心、风险监控、报告中心、设置。
5. 最后逐步接入真实数据、真实回测、真实信号、真实报告。

最终用户应该能通过本地启动命令打开一个高可视化量化研究平台，而不是继续依赖命令行。
