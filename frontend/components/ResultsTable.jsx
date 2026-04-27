function ResultsTable({ columns, rows }) {
  if (!columns.length) {
    return <p className="muted">No columns returned.</p>;
  }

  if (!rows.length) {
    return <p className="muted">Query ran successfully but returned no rows.</p>;
  }

  return (
    <div className="table-wrapper">
      <table>
        <thead>
          <tr>
            {columns.map((column) => (
              <th key={column}>{column}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, rowIndex) => (
            <tr key={`result-row-${rowIndex}`}>
              {columns.map((column) => (
                <td key={`${column}-${rowIndex}`}>{String(row[column] ?? "")}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default ResultsTable;
