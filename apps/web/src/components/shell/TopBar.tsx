import { Play, RefreshCw, Search } from "lucide-react";

export function TopBar() {
  return (
    <header className="top-bar">
      <div className="toolbar-left">
        <Search size={18} color="#8ea3bd" />
        <input className="search" placeholder="搜索标的 / 策略 / 指标 / 资讯" />
        <span className="pill">美股</span>
        <span className="pill">A股</span>
        <span className="pill">ETF</span>
        <span className="pill">日线</span>
      </div>
      <div className="toolbar-right">
        <button className="button"><RefreshCw size={15} /> 刷新数据</button>
        <button className="button"><Play size={15} /> 运行回测</button>
        <span className="badge positive">本地运行中</span>
      </div>
    </header>
  );
}
