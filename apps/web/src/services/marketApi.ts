import { fetchApi } from "./api";
import type { MarketSnapshot } from "../types/api";

export const getMarketSnapshot = (symbol = "510300", market = "a股etf", period = "1d") =>
  fetchApi<MarketSnapshot>(`/api/market/snapshot?symbol=${encodeURIComponent(symbol)}&market=${encodeURIComponent(market)}&period=${encodeURIComponent(period)}`);
