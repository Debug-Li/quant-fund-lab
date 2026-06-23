import type { ReactNode } from "react";

type PanelProps = {
  title?: string;
  action?: ReactNode;
  children: ReactNode;
  className?: string;
};

export function Panel({ title, action, children, className = "" }: PanelProps) {
  return (
    <section className={`panel ${className}`}>
      {(title || action) && (
        <div className="panel-header">
          <div className="panel-title">{title}</div>
          {action}
        </div>
      )}
      <div className="panel-body">{children}</div>
    </section>
  );
}
