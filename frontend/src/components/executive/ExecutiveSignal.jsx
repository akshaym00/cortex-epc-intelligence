import { severityLabel } from "../../utils/severity";

export default function ExecutiveSignal({ projectData }) {
  const impactedEntities = new Set(
    projectData.impacts?.flatMap((impact) =>
      (impact.impacted_entities || []).map((entity) => entity.name),
    ) || [],
  );

  const severityOrder = ["low", "medium", "high", "critical"];
  const riskLevel = (projectData.impacts || []).reduce((highest, impact) => {
    return severityOrder.indexOf(impact.overall_severity) >
      severityOrder.indexOf(highest)
      ? impact.overall_severity
      : highest;
  }, "low");

  const maxExposure = Math.max(
    ...(projectData.impacts || []).map(
      (impact) => impact.projected_completion_impact_days || 0,
    ),
    0,
  );

  const criticalPath =
    (projectData.impacts || [])
      .flatMap((impact) => impact.impacted_entities || [])
      .find((entity) => entity.critical_path && entity.dependency_path?.length)
      ?.dependency_path || [];

  const blockedGates = (projectData.controls_brief?.blocked_gates || []).length;

  const primaryMetrics = [
    {
      label: "Critical Path Delay",
      value: `${maxExposure}d`,
      type: "number",
      icon: "⏱",
    },
    {
      label: "Risk Level",
      value: severityLabel(riskLevel),
      type: "severity",
      icon: "⚠",
    },
  ];

  const secondaryMetrics = [
    {
      label: "Recovery Potential",
      value: `${Math.max(1, Math.round(maxExposure * 0.4))}d`,
      type: "number",
      icon: "📈",
    },
    { label: "Blocked Milestones", value: blockedGates, type: "number", icon: "🚧" },
    {
      label: "Confidence",
      value: `${projectData.controls_brief?.confidence || 85}%`,
      type: "number",
      icon: "✓",
    },
    {
      label: "Project Status",
      value: riskLevel,
      type: "status",
      icon: "🎯",
    },
  ];

  return (
    <section className="executive-signal">
      <div className="signal-header">
        <div>
          <h2>Executive Project Signal</h2>
          <p>Real-time project health and critical decisions</p>
        </div>
      </div>
      <div className="signal-primary-grid">
        {primaryMetrics.map((metric) => (
          <div key={metric.label} className={`signal-metric signal-primary signal-${metric.type}`}>
            <span className="metric-icon">{metric.icon}</span>
            <span className="metric-label">{metric.label}</span>
            <strong className={metric.type === "severity" ? `risk-${riskLevel}` : ""}>
              {metric.value}
            </strong>
          </div>
        ))}
      </div>
      <div className="signal-secondary-grid">
        {secondaryMetrics.map((metric) => (
          <div key={metric.label} className={`signal-metric signal-secondary signal-${metric.type}`}>
            <span className="metric-icon">{metric.icon}</span>
            <span className="metric-label">{metric.label}</span>
            <strong className={metric.type === "severity" ? `risk-${riskLevel}` : ""}>
              {metric.value}
            </strong>
          </div>
        ))}
      </div>
    </section>
  );
}
