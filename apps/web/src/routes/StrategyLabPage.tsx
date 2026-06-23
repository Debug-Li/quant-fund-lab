import { Panel } from "../components/layout/Panel";
import { PageHeader } from "../components/shell/PageHeader";
import { DataTable } from "../components/tables/DataTable";
import { getStrategyLab } from "../services/genericApi";
import { LoadingState } from "./LoadingState";
import { useApiData } from "./useApiData";

export function StrategyLabPage() {
  const { data, error, loading } = useApiData(getStrategyLab);
  if (!data) return <LoadingState error={error} loading={loading} />;
  return (
    <>
      <PageHeader title="策略研究" desc="策略列表、代码预览、参数 schema 和最近运行记录。" />
      <div className="split-main">
        <Panel title="策略列表"><DataTable rows={data.strategies} /></Panel>
        <div className="grid">
          <Panel title="策略代码预览"><pre className="metric-label">{data.code}</pre></Panel>
          <Panel title="参数配置"><DataTable rows={data.params} /></Panel>
          <Panel title="最近运行"><DataTable rows={data.runs.map((message: string, idx: number) => ({ step: idx + 1, message }))} /></Panel>
        </div>
      </div>
    </>
  );
}
