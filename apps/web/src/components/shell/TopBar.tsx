import { FormEvent, useEffect, useState } from "react";
import { Play, RefreshCw, Search } from "lucide-react";
import { marketOptions, periodOptions, type MarketScope, type PeriodScope, type ResearchContext } from "../../types/research";

type TopBarProps = {
  context: ResearchContext;
  onMarketChange: (market: MarketScope) => void;
  onPeriodChange: (period: PeriodScope) => void;
  onSymbolChange: (symbol: string) => void;
  onRefresh: () => void;
  onRunBacktest: () => void;
};

export function TopBar({ context, onMarketChange, onPeriodChange, onSymbolChange, onRefresh, onRunBacktest }: TopBarProps) {
  const [query, setQuery] = useState(context.symbol);
  useEffect(() => {
    setQuery(context.symbol);
  }, [context.symbol]);
  const submitSearch = (event: FormEvent) => {
    event.preventDefault();
    const value = query.trim().toUpperCase();
    if (value) onSymbolChange(value);
  };
  return (
    <header className="top-bar">
      <form className="toolbar-left" onSubmit={submitSearch}>
        <Search size={18} color="#8ea3bd" />
        <input className="search" placeholder="搜索标的，如 510300 / SPY" value={query} onChange={(event) => setQuery(event.target.value)} />
        {(Object.keys(marketOptions) as MarketScope[]).map((key) => (
          <button className={`pill-button ${context.market === key ? "active" : ""}`} type="button" key={key} onClick={() => onMarketChange(key)}>
            {marketOptions[key].label}
          </button>
        ))}
        {(Object.keys(periodOptions) as PeriodScope[]).map((key) => (
          <button className={`pill-button ${context.period === key ? "active" : ""}`} type="button" key={key} onClick={() => onPeriodChange(key)}>
            {periodOptions[key].label}
          </button>
        ))}
      </form>
      <div className="toolbar-right">
        <button className="button" type="button" onClick={onRefresh}><RefreshCw size={15} /> 刷新数据</button>
        <button className="button" type="button" onClick={onRunBacktest}><Play size={15} /> 运行回测</button>
        <span className="badge positive">本地运行中</span>
      </div>
    </header>
  );
}
