import Icon from "../common/Icon";

function inferSpecTag(finding) {
  const text = `${finding.parameter || ""} ${finding.requirement_citation || ""} ${finding.submittal_citation || ""}`.toLowerCase();
  if (text.includes("ups")) return "UPS-01";
  return finding.parameter || "SPEC-01";
}

function actionText(finding) {
  if (finding.status === "deviation") {
    return "Reject current vendor submittal and request revised submission before procurement approval.";
  }

  return finding.recommendation || "Accept submittal and proceed with procurement review.";
}

function CompliancePanel({ id, findings = [] }) {
  return (
    <section id={id} className="card compliance-card">
      <div className="compliance-heading">
        <h3>Spec Compliance</h3>
        <span>{findings.length} finding{findings.length === 1 ? "" : "s"}</span>
      </div>

      {findings.length === 0 ? (
        <p>No numeric spec/submittal comparison detected.</p>
      ) : findings.map((finding) => (
        <article className={`executive-alert finding-${finding.status}`} key={finding.parameter}>
          <div className="alert-title-row">
            <div>
              <span className="alert-kicker">
                <Icon name={finding.status === "deviation" ? "alert" : "shield"} size={16} />
                {finding.status === "deviation" ? "SPECIFICATION DEVIATION" : "SPECIFICATION COMPLIANT"}
              </span>
              <h4>{inferSpecTag(finding)}</h4>
            </div>
            <span className={`alert-status status-${finding.status}`}>{finding.status}</span>
          </div>

          <div className="alert-metric-grid">
            <div>
              <span>Required</span>
              <strong>{finding.required_value}{finding.unit}</strong>
            </div>
            <div>
              <span>Submitted</span>
              <strong>{finding.submitted_value}{finding.unit}</strong>
            </div>
            <div>
              <span>Gap</span>
              <strong>{finding.deviation}{finding.unit}</strong>
            </div>
          </div>

          <div className="alert-recommendation">
            <span>Recommended Action</span>
            <strong>{actionText(finding)}</strong>
          </div>

          <div className="compliance-document-grid">
            <div>
              <span>Requirement</span>
              <strong>{finding.requirement_citation}</strong>
            </div>
            <div>
              <span>Submitted Document</span>
              <strong>{finding.submittal_citation}</strong>
            </div>
          </div>
        </article>
      ))}
    </section>
  );
}

export default CompliancePanel;
