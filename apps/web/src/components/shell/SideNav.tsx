import { Activity, BarChart3, Bell, Database, FileText, Gauge, Home, LineChart, PieChart, Settings, Shield } from "lucide-react";

export type PageKey = "dashboard" | "market" | "strategy" | "backtest" | "portfolio" | "signal" | "data" | "risk" | "reports" | "settings";

const items: Array<{ key: PageKey; label: string; icon: any }> = [
  { key: "dashboard", label: "总览", icon: Home },
  { key: "market", label: "市场看盘", icon: LineChart },
  { key: "strategy", label: "策略研究", icon: Activity },
  { key: "backtest", label: "回测分析", icon: BarChart3 },
  { key: "portfolio", label: "组合管理", icon: PieChart },
  { key: "signal", label: "信号中心", icon: Bell },
  { key: "data", label: "数据中心", icon: Database },
  { key: "risk", label: "风险监控", icon: Shield },
  { key: "reports", label: "报告中心", icon: FileText },
  { key: "settings", label: "设置", icon: Settings }
];

export function SideNav({ active, onChange }: { active: PageKey; onChange: (key: PageKey) => void }) {
  return (
    <aside className="side-nav">
      <div className="brand">
        <div className="brand-mark"><Gauge size={20} /></div>
        <div>
          <div className="brand-title">量观 Quant Lab</div>
          <div className="brand-subtitle">Local Quant Terminal</div>
        </div>
      </div>
      {items.map((item) => {
        const Icon = item.icon;
        return (
          <button className={`nav-button ${active === item.key ? "active" : ""}`} key={item.key} onClick={() => onChange(item.key)}>
            <Icon size={18} />
            <span>{item.label}</span>
          </button>
        );
      })}
    </aside>
  );
}
