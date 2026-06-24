export type MarketScope = "us" | "cn" | "etf";
export type PeriodScope = "1d" | "1wk" | "1mo";

export type ResearchContext = {
  market: MarketScope;
  period: PeriodScope;
  symbol: string;
  refreshKey: number;
};

export const marketOptions: Record<MarketScope, { label: string; apiMarket: string; defaultSymbol: string }> = {
  us: { label: "美股", apiMarket: "US", defaultSymbol: "SPY" },
  cn: { label: "A股", apiMarket: "a股股票", defaultSymbol: "000001" },
  etf: { label: "ETF", apiMarket: "a股etf", defaultSymbol: "510300" }
};

export const periodOptions: Record<PeriodScope, { label: string }> = {
  "1d": { label: "日线" },
  "1wk": { label: "周线" },
  "1mo": { label: "月线" }
};
