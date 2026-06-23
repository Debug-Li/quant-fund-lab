import ReactECharts from "echarts-for-react";
import { baseChart } from "./chartTheme";

export function VolumeChart({ bars, height = 150 }: { bars: Array<Record<string, any>>; height?: number }) {
  const option = {
    ...baseChart,
    grid: { left: 42, right: 24, top: 12, bottom: 28 },
    xAxis: { ...baseChart.xAxis, type: "category", data: bars.map((d) => d.time) },
    yAxis: { ...baseChart.yAxis, type: "value" },
    series: [{ name: "成交量", type: "bar", data: bars.map((d) => d.volume), itemStyle: { color: "#1677ff" } }]
  };
  return <ReactECharts option={option} style={{ height }} notMerge />;
}
