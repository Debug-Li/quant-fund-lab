export function LoadingState({ error, loading }: { error: string | null; loading: boolean }) {
  if (loading) return <div className="panel metric-card">正在加载 demo 数据...</div>;
  if (error) return <div className="panel metric-card negative">加载失败：{error}</div>;
  return null;
}
