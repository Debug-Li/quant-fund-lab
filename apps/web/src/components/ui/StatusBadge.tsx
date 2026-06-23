export function StatusBadge({ children, tone = "neutral" }: { children: string; tone?: "positive" | "negative" | "neutral" }) {
  return <span className={`badge ${tone}`}>{children}</span>;
}
