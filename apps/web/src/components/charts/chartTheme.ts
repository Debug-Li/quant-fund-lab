import { theme } from "../../theme/tokens";

export const baseChart = {
  backgroundColor: "transparent",
  textStyle: { color: theme.colors.textMuted },
  grid: { left: 42, right: 24, top: 28, bottom: 36 },
  tooltip: {
    trigger: "axis",
    backgroundColor: "rgba(6,16,31,0.94)",
    borderColor: theme.colors.border,
    textStyle: { color: theme.colors.text }
  },
  xAxis: {
    axisLine: { lineStyle: { color: theme.colors.border } },
    axisLabel: { color: theme.colors.textMuted }
  },
  yAxis: {
    splitLine: { lineStyle: { color: theme.colors.grid } },
    axisLabel: { color: theme.colors.textMuted }
  }
};

export const chartColors = [theme.colors.primary, theme.colors.cyan, theme.colors.positive, theme.colors.warning, "#5b8ff9", "#5ad8a6"];
