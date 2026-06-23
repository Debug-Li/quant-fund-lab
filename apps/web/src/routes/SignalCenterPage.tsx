import { Panel } from "../components/layout/Panel";
import { PageHeader } from "../components/shell/PageHeader";
import { DataTable } from "../components/tables/DataTable";
import { SignalTimeline } from "../components/timeline/SignalTimeline";
import { getSignals } from "../services/genericApi";
import { LoadingState } from "./LoadingState";
import { useApiData } from "./useApiData";

export function SignalCenterPage() {
  const { data, error, loading } = useApiData(getSignals);
  if (!data) return <LoadingState error={error} loading={loading} />;
  const summary = Object.entries(data.summary).map(([name, value]) => ({ name, value }));
  return (
    <>
      <PageHeader title="信号中心" desc="买入、卖出、风控、调仓和数据更新信号集中处理。" />
      <div className="grid cols-2">
        <Panel title="今日信号概览"><DataTable rows={summary} /></Panel>
        <Panel title="信号时间线"><SignalTimeline items={data.signals} /></Panel>
      </div>
      <Panel title="历史信号表"><DataTable rows={data.signals} /></Panel>
    </>
  );
}
