import ReactECharts from "echarts-for-react";

export function RadarChart({ data, height = 260 }: { data: Array<Record<string, any>>; height?: number }) {
  const option = {
    radar: { indicator: data.map((d) => ({ name: d.factor, max: 100 })), axisName: { color: "#8ea3bd" }, splitLine: { lineStyle: { color: "#1f3857" } } },
    series: [{ type: "radar", data: [{ value: data.map((d) => d.value), areaStyle: { color: "rgba(22,119,255,0.22)" } }] }]
  };
  return <ReactECharts option={option} style={{ height }} notMerge />;
}
