import ReactECharts from "echarts-for-react";
import type { RiskMetric } from "../../types/api";
import { baseChart } from "./chartTheme";

export function RiskBars({ data, height = 260 }: { data: RiskMetric[]; height?: number }) {
  const option = {
    ...baseChart,
    grid: { left: 88, right: 24, top: 12, bottom: 28 },
    xAxis: { ...baseChart.xAxis, type: "value" },
    yAxis: { ...baseChart.yAxis, type: "category", data: data.map((d) => d.name) },
    series: [{ type: "bar", data: data.map((d) => d.value), itemStyle: { color: "#1677ff" } }]
  };
  return <ReactECharts option={option} style={{ height }} notMerge />;
}
