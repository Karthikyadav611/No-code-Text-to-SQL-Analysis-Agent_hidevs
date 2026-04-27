import { useState } from "react";

import FileUploader from "../components/FileUploader";

function UploadPage({ datasets, onUploadComplete }) {
  const [lastUpload, setLastUpload] = useState(null);

  return (
    <section className="two-column">
      <div className="card">
        <h2>Upload Dataset</h2>
        <p className="muted">
          Supported formats: <code>.csv</code>, <code>.xlsx</code>, <code>.xls</code>.
        </p>
        <FileUploader
          onUploadSuccess={(payload) => {
            setLastUpload(payload);
            onUploadComplete();
          }}
        />

        {lastUpload ? (
          <div className="stack-gap">
            <h3>Last Upload Summary</h3>
            <p>
              <strong>MySQL Table:</strong> <code>{lastUpload.table_name}</code>
            </p>
            <p>
              <strong>Rows Imported:</strong> {lastUpload.row_count}
            </p>
            <p>
              <strong>Columns:</strong> {lastUpload.columns.join(", ")}
            </p>
            <div className="table-wrapper">
              <table>
                <thead>
                  <tr>
                    {lastUpload.columns.map((column) => (
                      <th key={column}>{column}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {lastUpload.preview.map((row, index) => (
                    <tr key={`${index}-${lastUpload.table_name}`}>
                      {lastUpload.columns.map((column) => (
                        <td key={`${column}-${index}`}>{String(row[column] ?? "")}</td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        ) : null}
      </div>

      <div className="card">
        <h2>Available Datasets</h2>
        {datasets.length === 0 ? (
          <p className="muted">No datasets uploaded yet.</p>
        ) : (
          <ul className="list">
            {datasets.map((dataset) => (
              <li key={dataset.id} className="list-item">
                <p>
                  <strong>{dataset.original_filename}</strong>
                </p>
                <p>
                  Table: <code>{dataset.table_name}</code>
                </p>
                <p>Rows: {dataset.row_count}</p>
                <p>Uploaded: {new Date(dataset.created_at).toLocaleString()}</p>
              </li>
            ))}
          </ul>
        )}
      </div>
    </section>
  );
}

export default UploadPage;
