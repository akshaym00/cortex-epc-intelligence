import React from "react";
import Icon from "./Icon";
import { severityLabel } from "../../utils/severity";

const unique = (values) => [...new Set(values.filter(Boolean))];

function getImpactPath(item) {
  const impacted = item.impacted_entities || [];
  const criticalImpact = impacted.find((impact) => impact.critical_path && impact.dependency_path?.length > 1);
  const impactWithPath = criticalImpact || impacted.find((impact) => impact.dependency_path?.length > 1);

  if (impactWithPath?.dependency_path?.length > 1) {
    return unique(impactWithPath.dependency_path);
  }

  if (impacted.length > 0) {
    return unique([item.event_title, ...impacted.map((impact) => impact.name)]);
  }

  return unique([item.event_title]);
}

function getForecastDelay(item) {
  return item.projected_completion_impact_days || item.delay_days || 0;
}

function getAffectedActivities(item) {
  return unique((item.impacted_entities || []).map((impact) => impact.name));
}

function inferConfidence(item) {
  if (typeof item.confidence === "number") return Math.round(item.confidence * 100);
  if ((item.impacted_entities || []).some((impact) => impact.critical_path)) return 92;
  return 86;
}

function inferOwner(item) {
  const text = `${item.title || ""} ${item.description || ""}`.toLowerCase();
  if (text.includes("submittal") || text.includes("vendor")) return text.includes("request") ? "Voltsafe" : "Electrical Consultant";
  if (text.includes("notify") || text.includes("team")) return "Electrical Consultant";
  if (text.includes("schedule") || text.includes("resequence")) return "Planning Engineer";
  if (text.includes("procurement") || text.includes("expedite")) return "Procurement Manager";
  return "Project Manager";
}

function inferDue(item) {
  const text = `${item.title || ""} ${item.description || ""}`.toLowerCase();
  if (text.includes("notify")) return "Before Procurement Approval";
  if (text.includes("submittal") || text.includes("reject") || item.priority === "high" || item.priority === "critical") return "Immediately";
  if (text.includes("procurement")) return "Before Procurement Approval";
  if (item.priority === "medium") return "This week";
  return "Monitor";
}

function recommendationTitle(title = "") {
  const clean = title.replace(/\.$/, "");
  if (/notify/i.test(clean)) return "Notify Impacted Teams";
  if (/submittal|spec|reject|vendor/i.test(clean)) return "Request Revised Vendor Submittal";
  return clean;
}

function recommendationBody(item) {
  const text = `${item.title || ""} ${item.description || ""}`.toLowerCase();
  if (text.includes("notify") || text.includes("team")) {
    return { label: "Issue revised schedule to:", bullets: ["Procurement", "Project Controls"] };
  }
  if (text.includes("submittal") || text.includes("spec") || text.includes("reject")) {
    return { label: "Target", bullets: ["UPS efficiency ≥96%"] };
  }
  if (text.includes("schedule") || text.includes("resequence")) {
    return { label: "Planning objective", bullets: ["Recover available float", "Protect procurement approval"] };
  }
  return { label: "Action detail", bullets: [item.description] };
}

function entityIcon(entityType) {
  return ({
    equipment: "package",
    risk: "alert",
    milestone: "calendar",
    team: "users",
    document: "fileCheck",
    vendor: "building",
    task: "check",
    issue: "alert",
    event: "clock",
  })[entityType] || "fileCheck";
}

function DashboardCard({ id, title, items = [], onEntityClick }) {
  const cardType = title.toLowerCase().replaceAll(" ", "-");
  const headingIcons = {
    Entities: "building",
    Relationships: "branch",
    Events: "clock",
    "Impact Analysis": "alert",
    Recommendations: "fileCheck",
  };

  return (
    <div id={id} className={`card dashboard-card card-${cardType}`}>
      <div className="card-heading">
        <div>
          <span className="card-heading-icon"><Icon name={headingIcons[title] || "fileCheck"} size={16} /></span>
          <h3>{title}</h3>
        </div>
        <span className="card-count">{items.length}</span>
      </div>

      {items.length === 0 ? (
        <p>No data available.</p>
      ) : (
        <ul>
          {items.map((item, index) => {
            const recommendation = item.priority ? recommendationBody(item) : null;
            const entityId = item.id || item.source_entity_id || item.target_entity_id;
            const renderClickableName = (name, id) => (
              <button
                type="button"
                className="entity-link"
                onClick={() => id && onEntityClick?.(id)}
              >
                {name}
              </button>
            );

            return (
              <li key={index}>
                {item.name && (
                  <>
                    <strong>
                      <span className="item-icon"><Icon name={entityIcon(item.entity_type)} size={16} /></span>
                      {renderClickableName(item.name, item.id)}
                    </strong>
                    <br />
                    <small>{item.entity_type}</small>
                    <br />
                    <span>{item.description}</span>
                    {item.reported_by && (
                      <div className="event-metadata">
                        <span><b>Reported by:</b> {item.reported_by}</span>
                        {item.affected_entities?.length > 0 && (
                          <span><b>Affected:</b> {item.affected_entities.join(", ")}</span>
                        )}
                      </div>
                    )}
                  </>
                )}

                {item.source && (
                  <>
                    <strong>
                      {item.source_entity_id
                        ? renderClickableName(item.source, item.source_entity_id)
                        : item.source}
                    </strong>
                    {" → "}
                    <strong>
                      {item.target_entity_id
                        ? renderClickableName(item.target, item.target_entity_id)
                        : item.target}
                    </strong>
                    <br />
                    <small>{item.relationship_type}</small>
                  </>
                )}

                {item.title && item.event_type && (
                  <>
                    <strong>{item.title}</strong>
                    <br />
                    <small>
                      {item.event_type} · <span className={`severity-badge severity-${item.severity}`}>{severityLabel(item.severity)}</span>
                    </small>
                    <br />
                    <span>{item.description}</span>
                  </>
                )}

                {item.summary && (
                  <div className="impact-hero">
                    <div className="impact-hero-topline">
                      <span>PROJECT IMPACT</span>
                      <span className={`severity-badge severity-${item.overall_severity}`}>
                        {severityLabel(item.overall_severity)}
                      </span>
                    </div>
                    <h4>Critical Path</h4>
                    <div className="critical-path-stack">
                      {getImpactPath(item).map((node, pathIndex, path) => (
                        <div className="path-step" key={`${node}-${pathIndex}`}>
                          <span className="path-node">{node}</span>
                          {pathIndex < path.length - 1 && <span className="path-arrow">↓</span>}
                        </div>
                      ))}
                    </div>
                    <div className="impact-kpis">
                      <div>
                        <span>Forecast Schedule Delay</span>
                        <strong>{getForecastDelay(item)} Days</strong>
                      </div>
                      <div>
                        <span>Severity</span>
                        <strong>{severityLabel(item.overall_severity)}</strong>
                      </div>
                    </div>
                    <div className="affected-activities">
                      <span>Affected activities</span>
                      <ul>
                        {getAffectedActivities(item).map((activity) => (
                          <li key={activity}>{activity}</li>
                        ))}
                      </ul>
                    </div>
                    <div className="confidence-row">
                      <span>Confidence</span>
                      <strong>{inferConfidence(item)}%</strong>
                    </div>
                  </div>
                )}

                {item.priority && (
                  <article className="action-card">
                    <div className="action-card-title">
                      <span className="action-check"><Icon name="check" size={15} /></span>
                      <strong>{recommendationTitle(item.title)}</strong>
                    </div>
                    <div className="action-meta-grid">
                      <span>Owner <b>{inferOwner(item)}</b></span>
                      <span>Priority <b className={`severity-badge severity-${item.priority}`}>{severityLabel(item.priority)}</b></span>
                      <span>Due <b>{inferDue(item)}</b></span>
                    </div>
                    <div className="action-detail">
                      <span>{recommendation.label}</span>
                      <ul>
                        {recommendation.bullets.map((bullet) => (
                          <li key={bullet}>{bullet}</li>
                        ))}
                      </ul>
                    </div>
                  </article>
                )}
              </li>
            );
          })}
        </ul>
      )}
    </div>
  );
}

export default DashboardCard;
