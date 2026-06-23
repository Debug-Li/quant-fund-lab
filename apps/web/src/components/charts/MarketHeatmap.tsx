import ReactECharts from "echarts-for-react";
import type { HeatmapItem } from "../../types/api";

export function MarketHeatmap({ data, height = 280 }: { data: HeatmapItem[]; height?: number }) {
  const option = {
    tooltip: { trigger: "item" },
    series: [
      {
        type: "treemap",
        roam: false,
        breadcrumb: { show: false },
        data: data.map((d) => ({
          name: `${d.name}\n${d.change > 0 ? "+" : ""}${d.change}%`,
          value: Math.max(10, d.volume ?? Math.abs(d.change) * 20),
          itemStyle: { color: d.change >= 0 ? `rgba(0,199,129,${0.35 + Math.min(Math.abs(d.change) / 4, 0.55)})` : `rgba(255,77,79,${0.35 + Math.min(Math.abs(d.change) / 4, 0.55)})` }
        })),
        label: { color: "#e6eef8", fontSize: 12 }
      }
    ]
  };
  return <ReactECharts option={option} style={{ height }} notMerge />;
}
