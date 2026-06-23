import { MetricCard } from "../components/cards/MetricCard";
import { DonutAllocationChart } from "../components/charts/DonutAllocationChart";
import { EquityCurveChart } from "../components/charts/EquityCurveChart";
import { HeatGridChart } from "../components/charts/HeatGridChart";
import { RadarChart } from "../components/charts/RadarChart";
import { RiskBars } from "../components/charts/RiskBars";
import { Panel } from "../components/layout/Panel";
import { PageHeader } from "../components/shell/PageHeader";
import { DataTable } from "../components/tables/DataTable";
import { getPortfolioOverview } from "../services/portfolioApi";
import { LoadingState } from "./LoadingState";
import { useApiData } from "./useApiData";

export function PortfolioPage() {
  const { data, error, loading } = useApiData(getPortfolioOverview);
  if (!data) return <LoadingState error={error} loading={loading} />;
  const corr = data.correlation.flatMap((row, y) => row.map((value, x) => ({ x: data.correlationLabels[x], y: data.correlationLabels[y], value })));
  return (
    <>
      <PageHeader title="组合管理" desc="持仓、资产配置、因子暴露、相关性、风险贡献和调仓建议。" />
      <div className="grid cols-3">{data.kpis.map((item) => <MetricCard key={item.title} item={item} />)}</div>
      <div className="grid cols-2" style={{ marginTop: 14 }}>
        <Panel title="组合净值"><EquityCurveChart data={data.equityCurve} /></Panel>
        <Panel title="资产配置"><DonutAllocationChart data={data.allocation} /></Panel>
        <Panel title="因子暴露雷达"><RadarChart data={data.factorExposure} /></Panel>
        <Panel title="相关性矩阵"><HeatGridChart data={corr} xKey="x" yKey="y" valueKey="value" /></Panel>
        <Panel title="风险贡献"><RiskBars data={data.riskContribution.map((d) => ({ name: d.name, value: d.value }))} /></Panel>
        <Panel title="调仓建议"><DataTable rows={data.rebalance} /></Panel>
      </div>
      <Panel title="持仓明细" className="" ><DataTable rows={data.holdings} /></Panel>
    </>
  );
}
