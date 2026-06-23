import { Panel } from "../components/layout/Panel";
import { PageHeader } from "../components/shell/PageHeader";
import { DataTable } from "../components/tables/DataTable";
import { getDataCenter } from "../services/genericApi";
import { LoadingState } from "./LoadingState";
import { useApiData } from "./useApiData";

export function DataCenterPage() {
  const { data, error, loading } = useApiData(getDataCenter);
  if (!data) return <LoadingState error={error} loading={loading} />;
  return (
    <>
      <PageHeader title="数据中心" desc="数据源状态、本地数据概览、质量检查和导出入口。" />
      <div className="grid cols-3">
        <Panel title="数据源状态"><DataTable rows={data.sources} /></Panel>
        <Panel title="本地数据概览"><DataTable rows={data.datasets} /></Panel>
        <Panel title="质量检查"><DataTable rows={data.quality} /></Panel>
      </div>
    </>
  );
}
