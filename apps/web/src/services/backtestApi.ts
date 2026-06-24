import { fetchApi } from "./api";
import type { BacktestData } from "../types/api";

export const runBacktest = (symbol = "510300", market = "a股etf", period = "1d") =>
  fetchApi<BacktestData>("/api/backtest/run", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ symbol, market, period })
  });
