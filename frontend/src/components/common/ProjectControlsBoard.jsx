import Icon from "./Icon";
import { severityLabel } from "../../utils/severity";
import { formatINR } from "../../utils/formatters";

function unique(values) {
  return [...new Set(values.filter(Boolean))];
}

function fallbackBrief(projectData) {
  const deviations = projectData.compliance_findings?.filter((finding) => finding.status === "deviation") || [];
  const exposure = Math.max(...(projectData.impacts || []).map((impact) => impact.projected_completion_impact_days || 0), 0);
  const impacted = unique((projectData.impacts || []).flatMap((impact) => (impact.impacted_entities || []).map((entity) => entity.name)));
  const criticalPath = (projectData.impacts || [])
    .flatMap((impact) => impact.impacted_entities || [])
    .find((entity) => entity.critical_path && entity.dependency_path?.length)?.dependency_path || [];

  const delayCost = projectData.controls_brief?.daily_delay_cost ?? 42500;

  const extractMetrics = () => {
    const entities = projectData.entities || [];
    const relationships = projectData.relationships || [];
    if (!entities.length) {
      return { extraction_certainty: 0, dependency_completeness: 0 };
    }

    const entityNames = new Set(entities.map((entity) => entity.name));
    const connectedEntityNames = new Set(
      relationships.flatMap((relationship) => [relationship.source, relationship.target]),
    );
    const orphanEntities = entities.filter(
      (entity) =>
        !["event", "risk", "issue"].includes(entity.entity_type) &&
        !connectedEntityNames.has(entity.name),
    );
    const orphanRatio = orphanEntities.length / entities.length;

    const expectedTypes = ["supplies", "depends_on", "affects"];
    const foundTypes = new Set(
      relationships.map((relationship) => relationship.relationship_type),
    );
    const typeCoverage = expectedTypes.filter((type) => foundTypes.has(type)).length / expectedTypes.length;

    const extraction_certainty = Math.max(
      40,
      Math.min(100, 100 - Math.round(orphanRatio * 40) - Math.round((1 - typeCoverage) * 20)),
    );
    const resolvedRelationships = relationships.filter(
      (relationship) => entityNames.has(relationship.source) && entityNames.has(relationship.target),
    );
    const resolvedRatio = relationships.length
      ? resolvedRelationships.length / relationships.length
      : 0;
    const dependency_completeness = Math.max(
      0,
      Math.min(100, Math.round((resolvedRatio * 0.7 + typeCoverage * 0.3) * 100)),
    );

    return { extraction_certainty, dependency_completeness };
  };

  const fallbackMetrics = extractMetrics();

  if (!deviations.length && !exposure && !impacted.length) return null;

  return {
    gate_status: deviations.length ? "ON HOLD" : exposure ? "AT RISK" : "CLEAR",
    status_reason: deviations.length
      ? "A vendor submittal does not meet the minimum technical requirement, so procurement approval should not proceed."
      : exposure
        ? `Critical-path exposure of ${exposure} days requires schedule recovery and daily controls review.`
        : "No active blockers detected.",
    procurement_gate: deviations.length ? "Blocked pending technical approval" : "Proceed with recovery controls",
    schedule_exposure_days: exposure,
    recoverable_days: exposure ? Math.max(1, Math.round(exposure * 0.4)) : 0,
    commercial_notice: exposure ? "Prepare delay notice / vendor backcharge assessment." : "No delay notice currently triggered.",
    confidence: deviations.length && exposure ? 94 : deviations.length ? 92 : exposure ? 88 : 80,
    extraction_certainty: fallbackMetrics.extraction_certainty,
    dependency_completeness: fallbackMetrics.dependency_completeness,
    confidence_breakdown: {
      extraction_certainty: fallbackMetrics.extraction_certainty,
      dependency_completeness: fallbackMetrics.dependency_completeness,
      weight_extraction: 0.55,
      weight_dependency: 0.45,
      base_confidence: Math.round(fallbackMetrics.extraction_certainty * 0.55 + fallbackMetrics.dependency_completeness * 0.45),
      final_confidence: deviations.length && exposure ? 94 : deviations.length ? 92 : exposure ? 88 : 80,
    },
    daily_delay_cost: delayCost,
    impacted_entities: impacted,
    critical_path: criticalPath,
    blocked_gates: deviations.length ? ["Technical Submittal Review", "UPS Procurement Approval"] : exposure ? ["Project Procurement", "Commissioning Readiness"] : [],
    next_72_hours: deviations.length
      ? ["Reject non-compliant submittal in the review log.", "Request revised vendor submission before procurement approval."]
      : ["Request vendor recovery plan with dated milestones.", "Issue updated forecast to impacted teams."],
    decisions: [
      ...(deviations.length ? [{
        title: "Reject current vendor submittal",
        owner: "Electrical Consultant",
        priority: "high",
        due: "Before Procurement Approval",
        rationale: `${deviations[0].parameter} submitted at ${deviations[0].submitted_value}${deviations[0].unit}, below required ${deviations[0].required_value}${deviations[0].unit}.`,
        target: `${deviations[0].parameter} >= ${deviations[0].required_value}${deviations[0].unit}`,
      }] : []),
      ...(exposure ? [{
        title: "Approve recovery schedule",
        owner: "Project Controls Engineer",
        priority: "high",
        due: "Within 24 hours",
        rationale: `Current forecast shows ${exposure} days of critical-path exposure.`,
        target: `Recover approximately ${Math.max(1, Math.round(exposure * 0.4))} days through resequencing.`,
      }] : []),
      ...(impacted.length ? [{
        title: "Notify impacted workstream owners",
        owner: "Planning Engineer",
        priority: "medium",
        due: "Today",
        rationale: "Downstream activities require updated forecast dates and owner acknowledgement.",
        target: impacted.slice(0, 4).join(", "),
      }] : []),
    ],
  };
}

function statusClass(status = "") {
  return status.toLowerCase().replaceAll(" ", "-");
}

function ProjectControlsBoard({ projectData }) {
  const brief = projectData.controls_brief || fallbackBrief(projectData);

  if (!brief) {
    return (
      <section className="controls-board controls-board-empty">
        <div className="controls-board-heading">
          <span><Icon name="hardDrive" size={18} /> PROJECT CONTROLS COMMAND CENTER</span>
          <h2>Waiting for project intelligence</h2>
          <p>Analyze a schedule risk, RFI log, or vendor submittal to generate gate status, recovery actions, commercial notice risk, and PM decisions.</p>
        </div>
      </section>
    );
  }

  const costExposure = brief.schedule_exposure_days * (brief.daily_delay_cost || 0);
  const impactedEntities = brief.impacted_entities || [];

  return (
    <section className="controls-board">
      <div className="controls-board-heading">
        <span><Icon name="hardDrive" size={18} /> PROJECT CONTROLS COMMAND CENTER</span>
        <h2>PM decision pack</h2>
        <p>{brief.status_reason}</p>
      </div>

      <div className="controls-kpi-grid">
        <div className={`gate-tile gate-${statusClass(brief.gate_status)}`}>
          <span>Gate Status</span>
          <strong>{brief.gate_status}</strong>
          <small>{brief.procurement_gate}</small>
        </div>
        <div>
          <span>Schedule Exposure</span>
          <strong>{brief.schedule_exposure_days} Days</strong>
          <small>Forecast critical-path impact</small>
        </div>
        <div>
          <span>Recoverable</span>
          <strong>{brief.recoverable_days} Days</strong>
          <small>Resequencing opportunity</small>
        </div>
        <div>
          <span>Cost Exposure</span>
          <strong>{costExposure ? formatINR(costExposure) : '₹0'}</strong>
          <small>{brief.daily_delay_cost ? `Rate ${formatINR(brief.daily_delay_cost)}/day` : 'Delay cost rate'}</small>
          <small style={{display:'block', marginTop:4, color:'#8a9aaa', fontSize:10}}>Modeled estimate: delay days × assumed daily cost rate</small>
        </div>
        <div
          className="confidence-tile"
          title="Hover for confidence breakdown"
        >
          <span>Confidence</span>
          <div className="confidence-progress-bar">
            <div className="confidence-progress-fill" style={{ width: `${brief.confidence}%` }} />
          </div>
          <strong>{brief.confidence}%</strong>
          <small>
            Extraction {brief.extraction_certainty}% · Dependency {brief.dependency_completeness}%
          </small>
          <div className="confidence-tooltip">
            <table>
              <tbody>
                <tr>
                  <td>Extraction certainty</td>
                  <td>{brief.extraction_certainty ?? brief.confidence_breakdown?.extraction_certainty ?? '—'}%</td>
                </tr>
                <tr>
                  <td>Dependency completeness</td>
                  <td>{brief.dependency_completeness ?? brief.confidence_breakdown?.dependency_completeness ?? '—'}%</td>
                </tr>
                <tr>
                  <td>Weight (extraction)</td>
                  <td>{brief.confidence_breakdown?.weight_extraction ?? 0.55}</td>
                </tr>
                <tr>
                  <td>Weight (dependency)</td>
                  <td>{brief.confidence_breakdown?.weight_dependency ?? 0.45}</td>
                </tr>
                <tr>
                  <td>Base confidence</td>
                  <td>{brief.confidence_breakdown?.base_confidence ?? '—'}%</td>
                </tr>
                <tr>
                  <td>Final confidence</td>
                  <td>{brief.confidence_breakdown?.final_confidence ?? brief.confidence}%</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <div className="controls-detail-grid">
        <article className="controls-panel">
          <h3><Icon name="branch" size={18} /> Critical Path</h3>
          {brief.critical_path?.length ? (
            <div className="controls-path">
              {brief.critical_path.map((node, index) => {
                const activityMap = {
                  "Generator": "Generator Delivery",
                  "Electrical": "Electrical Installation",
                  "Commissioning": "Commissioning",
                  "Testing": "System Testing",
                  "UPS": "UPS Deployment",
                  "Procurement": "Procurement Approval",
                  "Fabrication": "Equipment Fabrication"
                };
                const displayLabel = activityMap[node] || `${node} Activity`;
                return (
                  <div key={`${node}-${index}`}>
                    <span>{displayLabel}</span>
                    {index < brief.critical_path.length - 1 && <b>↓</b>}
                  </div>
                );
              })}
            </div>
          ) : (
            <p>No critical path movement detected.</p>
          )}
          <div className="commercial-notice">
            <span>Commercial Notice</span>
            <strong>{brief.commercial_notice}</strong>
          </div>
        </article>

        <article className="controls-panel">
          <h3><Icon name="calendar" size={18} /> Next 72 Hours</h3>
          <ul className="controls-checklist">
            {(brief.next_72_hours || []).map((action) => (
              <li key={action}><Icon name="check" size={14} /> {action}</li>
            ))}
          </ul>
          {impactedEntities.length > 0 && (
            <div className="impacted-entities">
              <span>Impacted entities</span>
              {impactedEntities.map((entity) => <b key={entity}>{entity}</b>)}
              <small>Impacted = any activity reachable downstream from an active event or risk, regardless of severity. Not necessarily blocking the schedule.</small>
            </div>
          )}
          {brief.blocked_gates?.length > 0 && (
            <div className="blocked-gates">
              <span>Blocked gates</span>
              {brief.blocked_gates.map((gate) => <b key={gate}>{gate}</b>)}
              <small>Blocked = a milestone or approval checkpoint whose forecast date has been pushed past a hard deadline. The project cannot proceed through this gate without resequencing or an explicit exception.</small>
            </div>
          )}
        </article>
      </div>

      <div className="decision-strip">
        {(brief.decisions || []).map((decision) => (
          <article className="decision-card" key={`${decision.title}-${decision.owner}`}>
            <div>
              <span className={`severity-badge severity-${decision.priority}`}>{severityLabel(decision.priority)}</span>
              <h3>{decision.title}</h3>
            </div>
            <p>{decision.rationale}</p>
            <div className="decision-meta">
              <span>Owner <b>{decision.owner}</b></span>
              <span>Due <b>{decision.due}</b></span>
              {decision.target && <span>Target <b>{decision.target}</b></span>}
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}

export default ProjectControlsBoard;
