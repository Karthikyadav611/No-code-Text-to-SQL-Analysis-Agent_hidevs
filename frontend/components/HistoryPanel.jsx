function HistoryPanel({ history }) {
  if (!history.length) {
    return <p className="muted">No query history yet.</p>;
  }

  return (
    <ul className="list">
      {history.map((item) => (
        <li key={item.id} className="list-item">
          <p>
            <strong>User Query:</strong> {item.user_query}
          </p>
          <p>
            <strong>SQL:</strong> <code>{item.generated_sql}</code>
          </p>
          <p>
            <strong>Status:</strong>{" "}
            <span className={item.status === "success" ? "badge-success" : "badge-error"}>
              {item.status}
            </span>
          </p>
          <p>
            <strong>Execution Time:</strong>{" "}
            {item.execution_time_ms !== null && item.execution_time_ms !== undefined
              ? `${item.execution_time_ms} ms`
              : "N/A"}
          </p>
          {item.error_message ? (
            <p className="error-text">
              <strong>Error:</strong> {item.error_message}
            </p>
          ) : null}
          <p className="muted">At: {new Date(item.created_at).toLocaleString()}</p>
        </li>
      ))}
    </ul>
  );
}

export default HistoryPanel;
