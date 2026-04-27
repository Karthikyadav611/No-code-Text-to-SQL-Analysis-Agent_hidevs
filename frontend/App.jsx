import { useCallback, useEffect, useState } from "react";

import AnalysisPage from "./pages/AnalysisPage";
import UploadPage from "./pages/UploadPage";
import { fetchDatasets, fetchHistory, fetchSchema } from "./services/api";

const TABS = [
  { key: "upload", label: "Upload Data" },
  { key: "analysis", label: "Analyze Data" }
];

function App() {
  const [activeTab, setActiveTab] = useState("upload");
  const [datasets, setDatasets] = useState([]);
  const [history, setHistory] = useState([]);
  const [schemaText, setSchemaText] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [loadError, setLoadError] = useState("");

  const loadMetadata = useCallback(async () => {
    setIsLoading(true);
    setLoadError("");
    try {
      const [datasetResponse, historyResponse, schemaResponse] = await Promise.all([
        fetchDatasets(),
        fetchHistory(),
        fetchSchema()
      ]);

      setDatasets(datasetResponse.datasets || []);
      setHistory(historyResponse.history || []);
      setSchemaText(schemaResponse.schema_text || "");
    } catch (error) {
      const detail = error.response?.data?.detail || error.message || "Failed to load metadata.";
      setLoadError(detail);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    loadMetadata();
  }, [loadMetadata]);

  return (
    <div className="app-shell">
      <header className="app-header">
        <p className="eyebrow">Production AI Agent</p>
        <h1>Text-to-SQL Analysis Agent</h1>
        <p className="subtext">
          Upload CSV/XLSX datasets, ask questions in plain English, and get SQL-powered answers.
        </p>
      </header>

      <nav className="tab-nav">
        {TABS.map((tab) => (
          <button
            key={tab.key}
            className={activeTab === tab.key ? "tab-button active" : "tab-button"}
            onClick={() => setActiveTab(tab.key)}
            type="button"
          >
            {tab.label}
          </button>
        ))}
      </nav>

      {loadError ? <p className="error-banner">{loadError}</p> : null}

      <main className="page-body">
        {activeTab === "upload" ? (
          <UploadPage
            datasets={datasets}
            onUploadComplete={async () => {
              await loadMetadata();
              setActiveTab("analysis");
            }}
          />
        ) : (
          <AnalysisPage
            datasets={datasets}
            history={history}
            schemaText={schemaText}
            metadataLoading={isLoading}
            onRefreshMetadata={loadMetadata}
          />
        )}
      </main>
    </div>
  );
}

export default App;
