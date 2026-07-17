import { useState } from "react";
import { uploadDocument, runDemoScenario } from "../../api/cortexApi";

function UploadPanel({ setProjectData }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [expanded, setExpanded] = useState(false);
  const [activeScenario, setActiveScenario] = useState(null);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (!file) return;
    setSelectedFile(file);
    setError("");
    setActiveScenario(null);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setError("Please select a document.");
      return;
    }

    try {
      setLoading(true);
      setError("");
      const response = await uploadDocument(selectedFile);
      setProjectData(response);
    } catch (err) {
      console.error(err);
      setError("Failed to analyze document. Ensure the backend is running.");
    } finally {
      setLoading(false);
    }
  };

  /**
   * Run a named demo scenario through the full backend pipeline.
   * Identical to uploading the corresponding bundled document.
   *
   * @param {"rfi"|"compliance"} scenario
   * @param {string} label  Human-readable scenario name for error messages
   */
  const handleDemoScenario = async (scenario, label) => {
    try {
      setLoading(true);
      setError("");
      setActiveScenario(scenario);

      const response = await runDemoScenario(scenario);
      setProjectData(response);
    } catch (err) {
      console.error(err);
      setError(
        `Failed to run the ${label} scenario. ` +
          "Ensure the backend API is running on port 8000."
      );
      setActiveScenario(null);
    } finally {
      setLoading(false);
    }
  };

  const loadingLabel = (scenario) => {
    if (!loading) return null;
    if (activeScenario === scenario) return "Processing…";
    return null;
  };

  return (
    <section
      className={`upload-card ${expanded ? "upload-card-expanded" : "upload-card-collapsed"}`}
    >
      <div className="upload-summary" onClick={() => setExpanded(!expanded)}>
        <div>
          <span className="section-kicker">DOCUMENT INTELLIGENCE</span>
          <h2>Analyze New Document</h2>
          <p>Click to {expanded ? "hide" : "show"} the upload panel.</p>
        </div>
        <button
          type="button"
          className="collapse-toggle"
          aria-expanded={expanded}
        >
          {expanded ? "Collapse" : "Expand"}
        </button>
      </div>

      {expanded && (
        <>
          <div className="upload-copy">
            <span className="section-kicker">DOCUMENT INTELLIGENCE</span>
            <h2>Ingest a project record</h2>
            <p>
              Analyze RFIs, vendor notices, schedules and technical submittals
              against the living project model.
            </p>
          </div>

          <div className="upload-controls">
            <label className="file-picker">
              <span className="file-icon">↥</span>
              <span>
                <strong>
                  {selectedFile ? selectedFile.name : "Select project document"}
                </strong>
                <small>PDF or TXT · project-controlled records</small>
              </span>
              <input type="file" onChange={handleFileChange} />
            </label>

            <button
              className="primary-action"
              onClick={handleUpload}
              disabled={loading}
            >
              {loading && !activeScenario ? (
                <>
                  <i className="button-spinner" /> Processing model...
                </>
              ) : (
                <>
                  Analyze document <span>→</span>
                </>
              )}
            </button>
          </div>

          <div className="demo-actions">
            <span>QUICK SCENARIOS</span>

            {/* Scenario 1 — Vendor Delay / RFI */}
            <button
              className={`stress-demo-button${activeScenario === "rfi" && loading ? " loading" : ""}`}
              onClick={() =>
                handleDemoScenario("rfi", "Verified 20-line RFI")
              }
              disabled={loading}
              title="Runs the full AI pipeline on a vendor delay / RFI document"
            >
              {activeScenario === "rfi" && loading ? (
                <>
                  <i className="button-spinner" /> {loadingLabel("rfi")}
                </>
              ) : (
                "▦ Verified 20-line RFI set"
              )}
            </button>

            {/* Scenario 2 — Specification Compliance */}
            <button
              className={`compliance-demo-button${activeScenario === "compliance" && loading ? " loading" : ""}`}
              onClick={() =>
                handleDemoScenario("compliance", "Spec Compliance")
              }
              disabled={loading}
              title="Runs the full AI pipeline on a UPS specification compliance document"
            >
              {activeScenario === "compliance" && loading ? (
                <>
                  <i className="button-spinner" /> {loadingLabel("compliance")}
                </>
              ) : (
                "◇ Spec compliance case"
              )}
            </button>
          </div>

          {error && <p className="upload-error">{error}</p>}
        </>
      )}
    </section>
  );
}

export default UploadPanel;
