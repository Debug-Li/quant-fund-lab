import ReactECharts from "echarts-for-react";
import { baseChart } from "./chartTheme";

export function CandlestickChart({ bars, height = 360 }: { bars: Array<Record<string, any>>; height?: number }) {
  const dates = bars.map((d) => d.time);
  const option = {
    ...baseChart,
    legend: { textStyle: { color: "#8ea3bd" } },
    xAxis: { ...baseChart.xAxis, type: "category", data: dates },
    yAxis: { ...baseChart.yAxis, type: "value", scale: true },
    dataZoom: [{ type: "inside" }],
    series: [
      {
        name: "K线",
        type: "candlestick",
        data: bars.map((d) => [d.open, d.close, d.low, d.high]),
        itemStyle: { color: "#00c781", color0: "#ff4d4f", borderColor: "#00c781", borderColor0: "#ff4d4f" }
      },
      { name: "MA5", type: "line", showSymbol: false, data: bars.map((d) => d.ma5), smooth: true },
      { name: "MA20", type: "line", showSymbol: false, data: bars.map((d) => d.ma20), smooth: true },
      { name: "MA60", type: "line", showSymbol: false, data: bars.map((d) => d.ma60), smooth: true }
    ]
  };
  return <ReactECharts option={option} style={{ height }} notMerge />;
}
