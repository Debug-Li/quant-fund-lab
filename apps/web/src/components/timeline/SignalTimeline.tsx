import type { SignalRow } from "../../types/api";

export function SignalTimeline({ items }: { items: SignalRow[] }) {
  return (
    <div className="terminal-list">
      {items.map((item, index) => (
        <div className="timeline-item" key={index}>
          <span>{String(item.time ?? "")}</span>
          <span>
            <b>{String(item.type ?? "信号")}</b> · {String(item.symbol ?? "")} · {String(item.note ?? item.action ?? "")}
          </span>
        </div>
      ))}
    </div>
  );
}
