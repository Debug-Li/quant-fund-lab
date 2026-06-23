import { MetricCard } from "../components/cards/MetricCard";
import { DonutAllocationChart } from "../components/charts/DonutAllocationChart";
import { EquityCurveChart } from "../components/charts/EquityCurveChart";
import { MarketHeatmap } from "../components/charts/MarketHeatmap";
import { RiskBars } from "../components/charts/RiskBars";
import { Panel } from "../components/layout/Panel";
import { PageHeader } from "../components/shell/PageHeader";
import { DataTable } from "../components/tables/DataTable";
import { SignalTimeline } from "../components/timeline/SignalTimeline";
import { getDashboardOverview } from "../services/dashboardApi";
import { LoadingState } from "./LoadingState";
import { useApiData } from "./useApiData";

export function DashboardPage() {
  const { data, error, loading } = useApiData(getDashboardOverview);
  if (!data) return <LoadingState error={error} loading={loading} />;
  return (
    <>
      <PageHeader title="总览" desc="组合、市场、风险、信号和任务日志的一屏式研究视图。" />
      <div className="grid cols-4">{data.kpis.slice(0, 4).map((item) => <MetricCard key={item.title} item={item} />)}</div>
      <div className="grid dashboard-grid" style={{ marginTop: 14 }}>
        <div className="grid">
          <Panel title="组合净值 vs 基准"><EquityCurveChart data={data.equityCurve} /></Panel>
          <div className="grid cols-2">
            <Panel title="市场热力图"><MarketHeatmap data={data.marketHeatmap} /></Panel>
            <Panel title="风险指标"><RiskBars data={data.riskMetrics} /></Panel>
          </div>
          <Panel title="最近交易记录"><DataTable rows={data.recentTrades} /></Panel>
        </div>
        <div className="grid">
          <Panel title="资产配置"><DonutAllocationChart data={data.allocation} /></Panel>
          <Panel title="今日市场情绪">
            <div className="metric-value neutral">{data.marketSentiment.score}</div>
            <div className="metric-label">市场状态：{String(data.marketSentiment.label)} · 广度 {String(data.marketSentiment.breadth)}%</div>
          </Panel>
          <Panel title="信号提醒"><SignalTimeline items={data.signals} /></Panel>
          <Panel title="运行日志"><DataTable rows={data.logs} /></Panel>
        </div>
      </div>
    </>
  );
}
