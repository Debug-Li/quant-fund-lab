import { MetricCard } from "../components/cards/MetricCard";
import { DistributionChart } from "../components/charts/DistributionChart";
import { HeatGridChart } from "../components/charts/HeatGridChart";
import { RiskBars } from "../components/charts/RiskBars";
import { Panel } from "../components/layout/Panel";
import { PageHeader } from "../components/shell/PageHeader";
import { DataTable } from "../components/tables/DataTable";
import { getRisk } from "../services/genericApi";
import { LoadingState } from "./LoadingState";
import { useApiData } from "./useApiData";

export function RiskMonitorPage() {
  const { data, error, loading } = useApiData(getRisk);
  if (!data) return <LoadingState error={error} loading={loading} />;
  const corr = data.correlation.flatMap((row: number[], y: number) => row.map((value, x) => ({ x: data.correlationLabels[x], y: data.correlationLabels[y], value })));
  return (
    <>
      <PageHeader title="风险监控" desc="回撤、VaR、CVaR、相关性、风险贡献和告警时间线。" />
      <div className="grid cols-3">{data.metrics.map((item: any) => <MetricCard key={item.title} item={item} />)}</div>
      <div className="grid cols-2" style={{ marginTop: 14 }}>
        <Panel title="VaR / CVaR 分布"><DistributionChart data={data.varDistribution} /></Panel>
        <Panel title="相关性矩阵"><HeatGridChart data={corr} xKey="x" yKey="y" valueKey="value" /></Panel>
        <Panel title="风险贡献"><RiskBars data={data.riskContribution} /></Panel>
        <Panel title="风控告警"><DataTable rows={data.alerts} /></Panel>
      </div>
      <Panel title="AI 风险摘要"><div className="metric-label">{data.summary}</div></Panel>
    </>
  );
}
