import ReactECharts from "echarts-for-react";

export function HeatGridChart({ data, xKey, yKey, valueKey, height = 260 }: { data: Array<Record<string, any>>; xKey: string; yKey: string; valueKey: string; height?: number }) {
  const xs = Array.from(new Set(data.map((d) => d[xKey])));
  const ys = Array.from(new Set(data.map((d) => d[yKey])));
  const option = {
    tooltip: {},
    grid: { left: 48, right: 24, top: 24, bottom: 36 },
    xAxis: { type: "category", data: xs, axisLabel: { color: "#8ea3bd" } },
    yAxis: { type: "category", data: ys, axisLabel: { color: "#8ea3bd" } },
    visualMap: { min: 0, max: 2.5, show: false, inRange: { color: ["#132c49", "#1677ff", "#00c781"] } },
    series: [{ type: "heatmap", data: data.map((d) => [xs.indexOf(d[xKey]), ys.indexOf(d[yKey]), d[valueKey]]) }]
  };
  return <ReactECharts option={option} style={{ height }} notMerge />;
}
