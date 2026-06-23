import ReactECharts from "echarts-for-react";
import { baseChart } from "./chartTheme";

export function RsiChart({ bars, height = 140 }: { bars: Array<Record<string, any>>; height?: number }) {
  const option = {
    ...baseChart,
    grid: { left: 42, right: 24, top: 14, bottom: 28 },
    xAxis: { ...baseChart.xAxis, type: "category", data: bars.map((d) => d.time) },
    yAxis: { ...baseChart.yAxis, type: "value", min: 0, max: 100 },
    series: [{ name: "RSI", type: "line", showSymbol: false, data: bars.map((d) => d.rsi), areaStyle: { opacity: 0.12 } }]
  };
  return <ReactECharts option={option} style={{ height }} notMerge />;
}
