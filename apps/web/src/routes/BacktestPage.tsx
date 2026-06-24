import { MetricCard } from "../components/cards/MetricCard";
import { DistributionChart } from "../components/charts/DistributionChart";
import { EquityCurveChart } from "../components/charts/EquityCurveChart";
import { HeatGridChart } from "../components/charts/HeatGridChart";
import { Panel } from "../components/layout/Panel";
import { PageHeader } from "../components/shell/PageHeader";
import { DataTable } from "../components/tables/DataTable";
import { runBacktest } from "../services/backtestApi";
import { marketOptions, type ResearchContext } from "../types/research";
import { LoadingState } from "./LoadingState";
import { useApiData } from "./useApiData";

export function BacktestPage({ context }: { context: ResearchContext }) {
  const apiMarket = marketOptions[context.market].apiMarket;
  const { data, error, loading } = useApiData(
    () => runBacktest(context.symbol, apiMarket, context.period),
    [context.symbol, apiMarket, context.period, context.refreshKey]
  );
  if (!data) return <LoadingState error={error} loading={loading} />;
  return (
    <>
      <PageHeader title="回测分析" desc={`当前回测：${context.symbol} · ${marketOptions[context.market].label} · ${context.period}`} />
      <div className="grid cols-3">{data.kpis.slice(0, 6).map((item) => <MetricCard key={item.title} item={item} />)}</div>
      <div className="split-main" style={{ marginTop: 14 }}>
        <div className="grid">
          <Panel title={`${data.strategy} · 净值曲线`}><EquityCurveChart data={data.equityCurve} /></Panel>
          <div className="grid cols-2">
            <Panel title="参数寻优热力图"><HeatGridChart data={data.optimization} xKey="fast" yKey="slow" valueKey="sharpe" /></Panel>
            <Panel title="月度收益热力图"><DistributionChart data={data.monthlyReturns} /></Panel>
          </div>
          <Panel title="交易明细"><DataTable rows={data.trades} /></Panel>
        </div>
        <div className="grid">
          <Panel title="收益分布"><DistributionChart data={data.distribution} /></Panel>
          <Panel title="运行日志"><div className="terminal-list">{data.logs.map((log) => <div className="timeline-item" key={log}><span>step</span><span>{log}</span></div>)}</div></Panel>
          <Panel title="策略说明"><div className="metric-label">当前接口已优先接入本地真实行情和 MA Cross 回测引擎；缺少行情或数据源失败时自动回退 demo，页面不会空白。</div></Panel>
        </div>
      </div>
    </>
  );
}
