import { useState } from "react";
import { AppShell } from "./components/shell/AppShell";
import type { PageKey } from "./components/shell/SideNav";
import { BacktestPage } from "./routes/BacktestPage";
import { DashboardPage } from "./routes/DashboardPage";
import { DataCenterPage } from "./routes/DataCenterPage";
import { MarketWatchPage } from "./routes/MarketWatchPage";
import { PortfolioPage } from "./routes/PortfolioPage";
import { ReportsPage } from "./routes/ReportsPage";
import { RiskMonitorPage } from "./routes/RiskMonitorPage";
import { SettingsPage } from "./routes/SettingsPage";
import { SignalCenterPage } from "./routes/SignalCenterPage";
import { StrategyLabPage } from "./routes/StrategyLabPage";
import { marketOptions, type MarketScope, type PeriodScope, type ResearchContext } from "./types/research";

function renderPage(page: PageKey, context: ResearchContext) {
  switch (page) {
    case "dashboard":
      return <DashboardPage />;
    case "market":
      return <MarketWatchPage context={context} />;
    case "strategy":
      return <StrategyLabPage />;
    case "backtest":
      return <BacktestPage context={context} />;
    case "portfolio":
      return <PortfolioPage />;
    case "signal":
      return <SignalCenterPage />;
    case "data":
      return <DataCenterPage />;
    case "risk":
      return <RiskMonitorPage />;
    case "reports":
      return <ReportsPage />;
    case "settings":
      return <SettingsPage />;
  }
}

export default function App() {
  const [page, setPage] = useState<PageKey>("dashboard");
  const [context, setContext] = useState<ResearchContext>({ market: "etf", period: "1d", symbol: "510300", refreshKey: 0 });
  const updateMarket = (market: MarketScope) => {
    setContext((current) => ({
      ...current,
      market,
      symbol: marketOptions[market].defaultSymbol,
      refreshKey: current.refreshKey + 1
    }));
    setPage("market");
  };
  const updatePeriod = (period: PeriodScope) => {
    setContext((current) => ({ ...current, period, refreshKey: current.refreshKey + 1 }));
  };
  const updateSymbol = (symbol: string) => {
    setContext((current) => ({ ...current, symbol, refreshKey: current.refreshKey + 1 }));
    setPage("market");
  };
  const refresh = () => setContext((current) => ({ ...current, refreshKey: current.refreshKey + 1 }));
  const runBacktest = () => {
    setContext((current) => ({ ...current, refreshKey: current.refreshKey + 1 }));
    setPage("backtest");
  };
  return (
    <AppShell
      active={page}
      context={context}
      onChange={setPage}
      onMarketChange={updateMarket}
      onPeriodChange={updatePeriod}
      onSymbolChange={updateSymbol}
      onRefresh={refresh}
      onRunBacktest={runBacktest}
    >
      {renderPage(page, context)}
    </AppShell>
  );
}
