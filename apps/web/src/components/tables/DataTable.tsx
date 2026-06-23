type DataTableProps = {
  rows: Array<Record<string, unknown>>;
  columns?: string[];
};

export function DataTable({ rows, columns }: DataTableProps) {
  if (!rows?.length) {
    return <div className="metric-label">暂无数据</div>;
  }
  const cols = columns ?? Object.keys(rows[0]);
  return (
    <table className="table">
      <thead>
        <tr>{cols.map((col) => <th key={col}>{col}</th>)}</tr>
      </thead>
      <tbody>
        {rows.map((row, index) => (
          <tr key={index}>
            {cols.map((col) => (
              <td key={col}>{String(row[col] ?? "")}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}
