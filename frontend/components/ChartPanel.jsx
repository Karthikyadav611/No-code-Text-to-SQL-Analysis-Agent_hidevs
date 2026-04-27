import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis
} from "recharts";

function ChartPanel({ columns, rows }) {
  if (!rows.length || !columns.length) {
    return null;
  }

  const numericColumns = columns.filter((column) =>
    rows.some((row) => {
      const value = row[column];
      return value !== null && value !== "" && Number.isFinite(Number(value));
    })
  );

  if (!numericColumns.length) {
    return <p className="muted">No numeric columns detected for chart rendering.</p>;
  }

  const valueColumn = numericColumns[0];
  const labelColumn = columns.find((column) => column !== valueColumn) || columns[0];

  const chartData = rows.slice(0, 20).map((row, index) => ({
    label: String(row[labelColumn] ?? `Row ${index + 1}`),
    value: Number(row[valueColumn] ?? 0)
  }));

  return (
    <div className="chart-panel">
      <h3>
        Chart Preview ({valueColumn} by {labelColumn})
      </h3>
      <div className="chart-wrapper">
        <ResponsiveContainer width="100%" height={280}>
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="label" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="value" fill="#17896e" radius={[6, 6, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default ChartPanel;
