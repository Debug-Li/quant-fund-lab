import type { KpiCard } from "../../types/api";

export function MetricCard({ item }: { item: KpiCard }) {
  const statusClass = item.status === "positive" ? "positive" : item.status === "negative" ? "negative" : "neutral";
  return (
    <div className="panel metric-card">
      <div className="metric-label">{item.title}</div>
      <div className="metric-value">
        {item.value}
        {item.unit ? <span className="metric-label"> {item.unit}</span> : null}
      </div>
      <div className={`metric-delta ${statusClass}`}>
        {item.delta !== undefined ? `${item.delta > 0 ? "+" : ""}${item.delta}%` : "实时"}
        {item.deltaLabel ? ` · ${item.deltaLabel}` : ""}
      </div>
    </div>
  );
}
