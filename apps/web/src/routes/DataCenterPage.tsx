import { useState } from "react";
import { Panel } from "../components/layout/Panel";
import { PageHeader } from "../components/shell/PageHeader";
import { DataTable } from "../components/tables/DataTable";
import { downloadRealData, generateDemoData, getDataCenter } from "../services/genericApi";
import { LoadingState } from "./LoadingState";
import { useApiData } from "./useApiData";

export function DataCenterPage() {
  const { data, error, loading } = useApiData(getDataCenter);
  const [current, setCurrent] = useState<any | null>(null);
  const [message, setMessage] = useState("");
  const [busy, setBusy] = useState(false);
  const view = current ?? data;
  const runAction = async (action: "download" | "demo") => {
    setBusy(true);
    setMessage(action === "download" ? "正在下载真实 AKShare ETF 数据..." : "正在生成本地演示数据...");
    try {
      const next = action === "download" ? await downloadRealData() : await generateDemoData();
      setCurrent(next);
      setMessage(action === "download" ? "真实数据下载完成，已刷新本地数据状态。" : "演示数据生成完成，已刷新本地数据状态。");
    } catch (err) {
      setMessage(err instanceof Error ? err.message : "数据操作失败");
    } finally {
      setBusy(false);
    }
  };
  if (!view) return <LoadingState error={error} loading={loading} />;
  return (
    <>
      <PageHeader title="数据中心" desc="数据源状态、本地数据概览、质量检查和导出入口。" />
      <Panel
        title="数据操作"
        action={
          <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
            <button className="button" disabled={busy} onClick={() => runAction("download")}>下载真实 AKShare 数据</button>
            <button className="button" disabled={busy} onClick={() => runAction("demo")}>生成本地演示数据</button>
          </div>
        }
      >
        <div className="metric-label">{message || "真实数据优先写入 data/raw 与 data/processed；网络不可用时可先生成本地演示数据。所有操作只用于研究，不会连接交易下单。"}</div>
      </Panel>
      <div className="grid cols-3">
        <Panel title="数据源状态"><DataTable rows={view.sources} /></Panel>
        <Panel title="本地数据概览"><DataTable rows={view.datasets} /></Panel>
        <Panel title="质量检查"><DataTable rows={view.quality} /></Panel>
      </div>
    </>
  );
}
