import { fetchApi } from "./api";
import type { BacktestData } from "../types/api";

export const runBacktest = () =>
  fetchApi<BacktestData>("/api/backtest/run", {
    method: "POST"
  });
