import { useState } from "react";

import ChartPanel from "../components/ChartPanel";
import ChatQueryBox from "../components/ChatQueryBox";
import HistoryPanel from "../components/HistoryPanel";
import ResultsTable from "../components/ResultsTable";
import { runQuery } from "../services/api";

function createMessage(role, text) {
  return {
    id: `${Date.now()}-${Math.random().toString(16).slice(2)}`,
    role,
    text
  };
}

function AnalysisPage({ datasets, history, schemaText, metadataLoading, onRefreshMetadata }) {
  const [messages, setMessages] = useState([
    createMessage(
      "assistant",
      "Ask a question about your uploaded data, for example: Which region has the highest revenue?"
    )
  ]);
  const [queryError, setQueryError] = useState("");
  const [queryLoading, setQueryLoading] = useState(false);
  const [queryResult, setQueryResult] = useState(null);

  async function handleSubmitQuestion(question) {
    setQueryError("");
    setQueryLoading(true);
    setMessages((prev) => [...prev, createMessage("user", question)]);

    try {
      const result = await runQuery(question);
      setQueryResult(result);
      setMessages((prev) => [
        ...prev,
        createMessage(
          "assistant",
          `Generated SQL executed in ${result.execution_time_ms} ms and returned ${result.row_count} rows.`
        )
      ]);
      await onRefreshMetadata();
    } catch (error) {
      const detail =
        error.response?.data?.detail || error.message || "Query failed due to an unexpected error.";
      setQueryError(detail);
      setMessages((prev) => [...prev, createMessage("assistant", `Query failed: ${detail}`)]);
    } finally {
      setQueryLoading(false);
    }
  }

  return (
    <section className="analysis-layout">
      <div className="card">
        <h2>Natural Language Query</h2>
        <p className="muted">
          Uploaded tables available: {datasets.length}. Ask in plain language and the agent will
          generate safe SQL.
        </p>

        <div className="chat-window">
          {messages.map((message) => (
            <div
              key={message.id}
              className={message.role === "user" ? "chat-bubble user" : "chat-bubble assistant"}
            >
              {message.text}
            </div>
          ))}
        </div>

        <ChatQueryBox onSubmit={handleSubmitQuestion} isLoading={queryLoading || metadataLoading} />

        {queryError ? <p className="error-text">{queryError}</p> : null}

        <details className="schema-panel">
          <summary>View Current Schema Sent to LLM</summary>
          <pre>{schemaText || "No schema detected yet."}</pre>
        </details>
      </div>

      <div className="card">
        <h2>Query Output</h2>
        {queryResult ? (
          <div className="stack-gap">
            <p>
              <strong>Generated SQL:</strong>
            </p>
            <pre className="sql-block">{queryResult.sql}</pre>
            {queryResult.limit_applied ? (
              <p className="muted">
                Safety note: backend applied a row limit to prevent very large responses.
              </p>
            ) : null}
            <ResultsTable columns={queryResult.columns} rows={queryResult.rows} />
            <ChartPanel columns={queryResult.columns} rows={queryResult.rows} />
          </div>
        ) : (
          <p className="muted">Run a query to see tabular and chart results.</p>
        )}
      </div>

      <div className="card">
        <h2>Query History</h2>
        <HistoryPanel history={history} />
      </div>
    </section>
  );
}

export default AnalysisPage;
