import ReactECharts from "echarts-for-react";
import { baseChart } from "./chartTheme";

export function DistributionChart({ data, height = 240 }: { data: Array<Record<string, any>>; height?: number }) {
  const option = {
    ...baseChart,
    xAxis: { ...baseChart.xAxis, type: "category", data: data.map((d) => d.bucket ?? d.month) },
    yAxis: { ...baseChart.yAxis, type: "value" },
    series: [{ type: "bar", data: data.map((d) => d.value ?? d.return), itemStyle: { color: "#13c2c2" } }]
  };
  return <ReactECharts option={option} style={{ height }} notMerge />;
}
