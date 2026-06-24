import { fetchApi } from "./api";
import type { MarketSnapshot } from "../types/api";

export const getMarketSnapshot = (symbol = "510300") => fetchApi<MarketSnapshot>(`/api/market/snapshot?symbol=${symbol}&market=a%E8%82%A1etf`);
