import ReactECharts from "echarts-for-react";
import type { TimeSeriesPoint } from "../../types/api";
import { baseChart, chartColors } from "./chartTheme";

export function EquityCurveChart({ data, height = 320 }: { data: TimeSeriesPoint[]; height?: number }) {
  const option = {
    ...baseChart,
    color: chartColors,
    legend: { textStyle: { color: "#8ea3bd" } },
    xAxis: { ...baseChart.xAxis, type: "category", data: data.map((d) => d.time) },
    yAxis: { ...baseChart.yAxis, type: "value", scale: true },
    series: [
      { name: "组合净值", type: "line", smooth: true, showSymbol: false, data: data.map((d) => d.portfolio ?? d.equity ?? d.value) },
      { name: "基准", type: "line", smooth: true, showSymbol: false, data: data.map((d) => d.benchmark) }
    ]
  };
  return <ReactECharts option={option} style={{ height }} notMerge />;
}
