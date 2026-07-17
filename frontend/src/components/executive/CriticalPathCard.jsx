export default function CriticalPathCard({ projectData }) {
  const criticalPath =
    (projectData.impacts || [])
      .flatMap((impact) => impact.impacted_entities || [])
      .find((entity) => entity.critical_path && entity.dependency_path?.length)
      ?.dependency_path || [];

  const maxExposure = Math.max(
    ...(projectData.impacts || []).map(
      (impact) => impact.projected_completion_impact_days || 0,
    ),
    0,
  );

  const activityMap = {
    Generator: "Generator Delivery",
    Electrical: "Electrical Installation",
    Commissioning: "Commissioning",
    Testing: "System Testing",
    UPS: "UPS Deployment",
    Procurement: "Procurement Approval",
    Fabrication: "Equipment Fabrication",
  };

  const getActivityLabel = (node) => activityMap[node] || `${node} Activity`;

  return (
    <section className="critical-path-card">
      <div className="card-header-section">
        <h3>Critical Path</h3>
        {maxExposure > 0 && (
          <div className="exposure-badge">
            <span>{maxExposure} days exposure</span>
          </div>
        )}
      </div>

      {criticalPath && criticalPath.length > 0 ? (
        <div className="path-visualization">
          {criticalPath.map((node, index) => (
            <div key={`${node}-${index}`} className="path-step">
              <div className="path-node">{getActivityLabel(node)}</div>
              {index < criticalPath.length - 1 && (
                <div className="path-arrow">↓</div>
              )}
            </div>
          ))}
        </div>
      ) : (
        <div className="path-empty">
          <p>No critical path movement detected.</p>
        </div>
      )}

      {projectData.controls_brief?.schedule_exposure_days > 0 && (
        <div className="exposure-summary">
          <div>
            <span>Schedule Slip</span>
            <strong>{projectData.controls_brief.schedule_exposure_days} days</strong>
          </div>
          <div>
            <span>Recoverable (40%)</span>
            <strong>{projectData.controls_brief.recoverable_days} days</strong>
          </div>
        </div>
      )}
    </section>
  );
}
