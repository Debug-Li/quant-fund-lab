import { Panel } from "../components/layout/Panel";
import { PageHeader } from "../components/shell/PageHeader";
import { DataTable } from "../components/tables/DataTable";
import { getReports } from "../services/genericApi";
import { LoadingState } from "./LoadingState";
import { useApiData } from "./useApiData";

export function ReportsPage() {
  const { data, error, loading } = useApiData(getReports);
  if (!data) return <LoadingState error={error} loading={loading} />;
  return (
    <>
      <PageHeader title="报告中心" desc="回测、信号、风险和数据导出的报告统一查看。" />
      <Panel title="报告列表"><DataTable rows={data.reports} /></Panel>
      <Panel title="报告预览"><div className="metric-label">选择报告后可预览 CSV、HTML 或图像产物。当前显示 demo 报告索引。</div></Panel>
    </>
  );
}
