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

function renderPage(page: PageKey) {
  switch (page) {
    case "dashboard":
      return <DashboardPage />;
    case "market":
      return <MarketWatchPage />;
    case "strategy":
      return <StrategyLabPage />;
    case "backtest":
      return <BacktestPage />;
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
  return (
    <AppShell active={page} onChange={setPage}>
      {renderPage(page)}
    </AppShell>
  );
}
