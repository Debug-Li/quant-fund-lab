import { Panel } from "../components/layout/Panel";
import { PageHeader } from "../components/shell/PageHeader";
import { DataTable } from "../components/tables/DataTable";
import { getSettings } from "../services/genericApi";
import { LoadingState } from "./LoadingState";
import { useApiData } from "./useApiData";

export function SettingsPage() {
  const { data, error, loading } = useApiData(getSettings);
  if (!data) return <LoadingState error={error} loading={loading} />;
  const rows = Object.entries(data)
    .filter(([, value]) => typeof value === "string")
    .map(([name, value]) => ({ name, value }));
  return (
    <>
      <PageHeader title="设置" desc="目录、默认市场、依赖、版本和 token 配置状态。" />
      <div className="grid cols-3">
        <Panel title="基础配置"><DataTable rows={rows} /></Panel>
        <Panel title="Token 状态"><DataTable rows={data.tokens} /></Panel>
        <Panel title="依赖检查"><DataTable rows={data.dependencies} /></Panel>
      </div>
    </>
  );
}
