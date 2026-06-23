export type ApiResponse<T> = {
  success: boolean;
  message: string;
  data: T;
  error?: string | null;
  logs?: string[];
};

export type KpiCard = {
  title: string;
  value: string | number;
  unit?: string;
  delta?: number;
  deltaLabel?: string;
  status: "positive" | "negative" | "neutral";
  sparkline?: TimeSeriesPoint[];
};

export type TimeSeriesPoint = {
  time: string;
  value?: number;
  portfolio?: number;
  benchmark?: number;
  equity?: number;
};

export type AllocationItem = {
  name: string;
  value: number;
  amount?: number;
};

export type HeatmapItem = {
  name: string;
  change: number;
  volume?: number;
};

export type RiskMetric = {
  name: string;
  value: number;
  threshold?: number;
  status?: string;
};

export type TradeRow = Record<string, string | number>;
export type SignalRow = Record<string, string | number>;

export type DashboardOverview = {
  demo: boolean;
  kpis: KpiCard[];
  equityCurve: TimeSeriesPoint[];
  allocation: AllocationItem[];
  marketHeatmap: HeatmapItem[];
  riskMetrics: RiskMetric[];
  recentTrades: TradeRow[];
  signals: SignalRow[];
  marketSentiment: Record<string, string | number>;
  capitalFlow: TimeSeriesPoint[];
  logs: Array<Record<string, string>>;
};

export type MarketSnapshot = {
  demo: boolean;
  symbol: string;
  name: string;
  price: number;
  changePct: number;
  bars: Array<Record<string, number | string>>;
  orderBook: {
    asks: Array<Record<string, number | string>>;
    bids: Array<Record<string, number | string>>;
  };
  watchlist: Array<Record<string, number | string>>;
  comparison: Array<{ symbol: string; series: TimeSeriesPoint[] }>;
  sectorFlow: HeatmapItem[];
  news: Array<Record<string, string>>;
  summary: string;
  signals: SignalRow[];
};

export type BacktestData = {
  demo: boolean;
  strategy: string;
  kpis: KpiCard[];
  equityCurve: TimeSeriesPoint[];
  optimization: Array<Record<string, number>>;
  monthlyReturns: Array<Record<string, number | string>>;
  distribution: Array<Record<string, number>>;
  trades: TradeRow[];
  logs: string[];
};

export type PortfolioData = {
  demo: boolean;
  kpis: KpiCard[];
  equityCurve: TimeSeriesPoint[];
  allocation: AllocationItem[];
  holdings: TradeRow[];
  factorExposure: Array<Record<string, number | string>>;
  correlation: number[][];
  correlationLabels: string[];
  riskContribution: AllocationItem[];
  rebalance: Array<Record<string, string>>;
};
