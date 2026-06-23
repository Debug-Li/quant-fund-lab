import type { ReactNode } from "react";
import { SideNav, type PageKey } from "./SideNav";
import { TopBar } from "./TopBar";

export function AppShell({ active, onChange, children }: { active: PageKey; onChange: (key: PageKey) => void; children: ReactNode }) {
  return (
    <div className="app-shell">
      <SideNav active={active} onChange={onChange} />
      <main className="main-area">
        <TopBar />
        <div className="content">{children}</div>
      </main>
    </div>
  );
}
