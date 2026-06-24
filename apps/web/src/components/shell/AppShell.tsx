import type { ReactNode } from "react";
import { SideNav, type PageKey } from "./SideNav";
import { TopBar } from "./TopBar";
import type { MarketScope, PeriodScope, ResearchContext } from "../../types/research";

type AppShellProps = {
  active: PageKey;
  context: ResearchContext;
  onChange: (key: PageKey) => void;
  onMarketChange: (market: MarketScope) => void;
  onPeriodChange: (period: PeriodScope) => void;
  onSymbolChange: (symbol: string) => void;
  onRefresh: () => void;
  onRunBacktest: () => void;
  children: ReactNode;
};

export function AppShell({ active, context, onChange, onMarketChange, onPeriodChange, onSymbolChange, onRefresh, onRunBacktest, children }: AppShellProps) {
  return (
    <div className="app-shell">
      <SideNav active={active} onChange={onChange} />
      <main className="main-area">
        <TopBar
          context={context}
          onMarketChange={onMarketChange}
          onPeriodChange={onPeriodChange}
          onSymbolChange={onSymbolChange}
          onRefresh={onRefresh}
          onRunBacktest={onRunBacktest}
        />
        <div className="content">{children}</div>
      </main>
    </div>
  );
}
