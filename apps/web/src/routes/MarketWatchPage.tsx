import { CandlestickChart } from "../components/charts/CandlestickChart";
import { MacdChart } from "../components/charts/MacdChart";
import { MarketHeatmap } from "../components/charts/MarketHeatmap";
import { RsiChart } from "../components/charts/RsiChart";
import { VolumeChart } from "../components/charts/VolumeChart";
import { EquityCurveChart } from "../components/charts/EquityCurveChart";
import { Panel } from "../components/layout/Panel";
import { PageHeader } from "../components/shell/PageHeader";
import { DataTable } from "../components/tables/DataTable";
import { SignalTimeline } from "../components/timeline/SignalTimeline";
import { getMarketSnapshot } from "../services/marketApi";
import { LoadingState } from "./LoadingState";
import { useApiData } from "./useApiData";

export function MarketWatchPage() {
  const { data, error, loading } = useApiData(() => getMarketSnapshot("NVDA"));
  if (!data) return <LoadingState error={error} loading={loading} />;
  return (
    <>
      <PageHeader title="市场看盘" desc="K线、盘口、自选股、板块资金和新闻信号集中看盘。" />
      <div className="split-main">
        <div className="grid">
          <Panel title={`${data.symbol} · ${data.name}`} action={<span className={data.changePct >= 0 ? "positive" : "negative"}>{data.price} · {data.changePct}%</span>}>
            <CandlestickChart bars={data.bars} />
          </Panel>
          <Panel title="成交量"><VolumeChart bars={data.bars} /></Panel>
          <div className="grid cols-2">
            <Panel title="MACD"><MacdChart bars={data.bars} /></Panel>
            <Panel title="RSI"><RsiChart bars={data.bars} /></Panel>
          </div>
          <Panel title="多标的对比">
            <EquityCurveChart data={data.comparison[0].series.map((point, idx) => ({ time: point.time, portfolio: point.value, benchmark: data.comparison[2].series[idx]?.value }))} height={260} />
          </Panel>
        </div>
        <div className="grid">
          <Panel title="盘口 · 模拟盘口，仅供研究"><DataTable rows={[...data.orderBook.asks, ...data.orderBook.bids]} /></Panel>
          <Panel title="自选股"><DataTable rows={data.watchlist} /></Panel>
          <Panel title="板块资金流"><MarketHeatmap data={data.sectorFlow} height={220} /></Panel>
          <Panel title="AI 市场摘要"><div className="metric-label">{data.summary}</div></Panel>
          <Panel title="新闻与信号"><SignalTimeline items={[...data.signals, ...data.news] as any} /></Panel>
        </div>
      </div>
    </>
  );
}
