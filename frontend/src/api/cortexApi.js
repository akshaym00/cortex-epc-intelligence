import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
});

/**
 * Upload a user-selected document and run the full analysis pipeline.
 * @param {File} file
 * @returns {Promise<object>} AnalyzeResponse
 */
export async function uploadDocument(file) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await api.post("/analyze", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });

  return response.data;
}

/**
 * Run the full analysis pipeline on a bundled demo scenario.
 * Behaves identically to uploading the corresponding document via uploadDocument().
 *
 * @param {"rfi"|"compliance"} scenario
 * @returns {Promise<object>} AnalyzeResponse
 */
export async function runDemoScenario(scenario) {
  const response = await api.get(`/analyze/demo/${scenario}`);
  return response.data;
}

export default api;