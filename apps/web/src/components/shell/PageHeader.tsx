export function PageHeader({ title, desc }: { title: string; desc: string }) {
  return (
    <div className="page-header">
      <div>
        <h1 className="page-title">{title}</h1>
        <p className="page-desc">{desc}</p>
      </div>
      <span className="badge">Demo 数据 · 不接入真实交易</span>
    </div>
  );
}
