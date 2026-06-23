import { fetchApi } from "./api";
import type { MarketSnapshot } from "../types/api";

export const getMarketSnapshot = (symbol = "NVDA") => fetchApi<MarketSnapshot>(`/api/market/snapshot?symbol=${symbol}`);
