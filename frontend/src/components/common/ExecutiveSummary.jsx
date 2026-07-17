import { severityLabel } from "../../utils/severity";

function ExecutiveSummary({ projectData }) {
  const impactedEntities = new Set(
    projectData.impacts.flatMap((impact) =>
      (impact.impacted_entities || []).map((entity) => entity.name),
    ),
  );

  const severityOrder = ["low", "medium", "high", "critical"];
  const riskLevel = projectData.impacts.reduce((highest, impact) => {
    return severityOrder.indexOf(impact.overall_severity) > severityOrder.indexOf(highest)
      ? impact.overall_severity
      : highest;
  }, "low");

  const metrics = [
    ["Risk level", riskLevel],
    ["Entities", projectData.entities.length],
    ["Relationships", projectData.relationships.length],
    ["Events", projectData.events.length],
    ["Impacted entities", impactedEntities.size],
    ["Recommendations", projectData.recommendations.length],
  ];

  return (
    <section className="executive-summary">
      <div className="summary-heading">
        <span>PROJECT HEALTH INDEX</span>
        <h2>Delivery outlook</h2>
        <p>Calculated from active events and downstream dependencies.</p>
      </div>
      <div className="summary-metrics">
        {metrics.map(([label, value], index) => (
          <div className="summary-metric" key={label}>
            <span>{label}</span>
            <strong className={index === 0 ? `risk-${value}` : ""}>
              {index === 0 ? severityLabel(value) : value}
            </strong>
          </div>
        ))}
      </div>
      {projectData.verification && (
        <div className="verification-chip">
          Verified run<br />
          <strong>{projectData.verification.elapsed_seconds}s</strong>
        </div>
      )}
    </section>
  );
}

export default ExecutiveSummary;
