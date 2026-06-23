import ReactECharts from "echarts-for-react";
import { baseChart } from "./chartTheme";

export function MacdChart({ bars, height = 160 }: { bars: Array<Record<string, any>>; height?: number }) {
  const option = {
    ...baseChart,
    grid: { left: 42, right: 24, top: 20, bottom: 28 },
    legend: { textStyle: { color: "#8ea3bd" } },
    xAxis: { ...baseChart.xAxis, type: "category", data: bars.map((d) => d.time) },
    yAxis: { ...baseChart.yAxis, type: "value" },
    series: [
      { name: "MACD", type: "line", showSymbol: false, data: bars.map((d) => d.macd) },
      { name: "Signal", type: "line", showSymbol: false, data: bars.map((d) => d.signal) }
    ]
  };
  return <ReactECharts option={option} style={{ height }} notMerge />;
}
