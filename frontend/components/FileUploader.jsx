import { useState } from "react";

import { uploadDataset } from "../services/api";

function FileUploader({ onUploadSuccess }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [successMessage, setSuccessMessage] = useState("");

  async function handleUpload() {
    if (!selectedFile) {
      setError("Please choose a file before uploading.");
      return;
    }

    setLoading(true);
    setError("");
    setSuccessMessage("");

    try {
      const payload = await uploadDataset(selectedFile);
      setSuccessMessage(
        `Upload complete. Imported ${payload.row_count} rows into ${payload.table_name}.`
      );
      onUploadSuccess(payload);
      setSelectedFile(null);
    } catch (uploadError) {
      const detail =
        uploadError.response?.data?.detail || uploadError.message || "Upload failed unexpectedly.";
      setError(detail);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="stack-gap">
      <input
        type="file"
        accept=".csv,.xlsx,.xls"
        onChange={(event) => {
          const file = event.target.files?.[0] || null;
          setSelectedFile(file);
          setError("");
          setSuccessMessage("");
        }}
      />
      <button type="button" className="primary-button" onClick={handleUpload} disabled={loading}>
        {loading ? "Uploading..." : "Upload File"}
      </button>
      {selectedFile ? <p className="muted">Selected: {selectedFile.name}</p> : null}
      {successMessage ? <p className="success-text">{successMessage}</p> : null}
      {error ? <p className="error-text">{error}</p> : null}
    </div>
  );
}

export default FileUploader;
