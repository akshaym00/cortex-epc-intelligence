import Icon from "./Icon";

function buildComplianceInsight(findings) {
  const deviation = findings.find((finding) => finding.status === "deviation");
  if (!deviation) return null;

  return `The uploaded vendor submittal violates the minimum ${deviation.parameter} requirement by ${Math.abs(Number(deviation.deviation) || 0)}${deviation.unit}.`;
}

function formatDelayText(days) {
  if (days === 1) return "one day";
  if (days === 7) return "one week";
  if (days % 7 === 0) return `${days / 7} weeks`;
  return `${days} days`;
}

function buildImpactInsight(impacts, blockedGates) {
  const impact = impacts.find((item) => item.projected_completion_impact_days || item.delay_days);
  if (!impact) return null;

  const days = impact.projected_completion_impact_days || impact.delay_days;
  const dayText = formatDelayText(days);
  const gate = blockedGates?.[0] || "critical approval gate";

  return `Critical ${gate} is blocked due to a ${days}-day delay; without recovery action, project handover is forecast to slip by approximately ${dayText}.`;
}

function AIInsight({ projectData }) {
  const complianceInsight = buildComplianceInsight(projectData.compliance_findings || []);
  const impactInsight = buildImpactInsight(projectData.impacts || [], projectData.controls_brief?.blocked_gates || []);
  const hasInsight = complianceInsight || impactInsight;

  return (
    <section className="ai-insight-card">
      <div className="insight-icon">
        <Icon name="shield" size={22} />
      </div>
      <div>
        <span>AI INSIGHT</span>
        <h2>Executive project signal</h2>
        <p>
          {hasInsight
            ? [complianceInsight, impactInsight].filter(Boolean).join(" ")
            : "Analyze a vendor submittal or project record to surface specification deviations, schedule risk, and recommended actions."}
        </p>
      </div>
    </section>
  );
}

export default AIInsight;
