import ReactECharts from "echarts-for-react";
import type { AllocationItem } from "../../types/api";
import { chartColors } from "./chartTheme";

export function DonutAllocationChart({ data, height = 260 }: { data: AllocationItem[]; height?: number }) {
  const option = {
    color: chartColors,
    tooltip: { trigger: "item" },
    legend: { bottom: 0, textStyle: { color: "#8ea3bd" } },
    series: [{ type: "pie", radius: ["48%", "72%"], center: ["50%", "45%"], data: data.map((d) => ({ name: d.name, value: d.value })) }]
  };
  return <ReactECharts option={option} style={{ height }} notMerge />;
}
