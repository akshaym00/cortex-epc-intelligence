export default function RiskSummary({ projectData }) {
  // Events from the pipeline are the source of risk/event data.
  // EventResponse fields: title, event_type, description, severity, reported_by, affected_entities
  const risks = projectData.events || [];

  // Group by severity level
  const risksByLevel = {
    critical: risks.filter(
      (r) => r.severity === "critical" || r.severity === "CRITICAL"
    ),
    high: risks.filter(
      (r) => r.severity === "high" || r.severity === "HIGH"
    ),
    medium: risks.filter(
      (r) => r.severity === "medium" || r.severity === "MEDIUM"
    ),
    low: risks.filter(
      (r) => r.severity === "low" || r.severity === "LOW"
    ),
  };

  const totalRisks = risks.length;

  return (
    <section className="risk-summary-card">
      <h3>Project Risks</h3>
      <p className="summary-intro">
        {totalRisks} identified risk{totalRisks !== 1 ? "s" : ""} and event
        {totalRisks !== 1 ? "s" : ""} across the project
      </p>

      <div className="risk-level-summary">
        {Object.entries(risksByLevel).map(([level, items]) => {
          if (items.length === 0) return null;

          return (
            <div key={level} className={`risk-level risk-level-${level}`}>
              <div className="level-header">
                <span className="level-badge">{level.toUpperCase()}</span>
                <strong className="level-count">{items.length}</strong>
              </div>
              <ul className="risk-items">
                {items.slice(0, 3).map((risk, idx) => (
                  <li key={idx}>
                    {/* Use title as primary label; description as supporting detail */}
                    <span className="risk-name">{risk.title}</span>
                    {risk.description && (
                      <span className="risk-timing">
                        {risk.description.length > 80
                          ? risk.description.slice(0, 80) + "…"
                          : risk.description}
                      </span>
                    )}
                  </li>
                ))}
                {items.length > 3 && (
                  <li className="more-risks">+{items.length - 3} more</li>
                )}
              </ul>
            </div>
          );
        })}
      </div>

      {totalRisks === 0 && (
        <div className="no-risks">
          <p>✓ No active risks detected</p>
        </div>
      )}
    </section>
  );
}
