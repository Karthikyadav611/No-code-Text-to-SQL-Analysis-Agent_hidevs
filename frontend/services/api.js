import axios from "axios";

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api",
  timeout: 60000
});

export async function uploadDataset(file) {
  const formData = new FormData();
  formData.append("file", file);
  const response = await apiClient.post("/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" }
  });
  return response.data;
}

export async function runQuery(question) {
  const response = await apiClient.post("/query", { question });
  return response.data;
}

export async function fetchSchema() {
  const response = await apiClient.get("/schema");
  return response.data;
}

export async function fetchDatasets() {
  const response = await apiClient.get("/datasets");
  return response.data;
}

export async function fetchHistory(limit = 50) {
  const response = await apiClient.get("/history", { params: { limit } });
  return response.data;
}
