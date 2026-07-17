import Icon from "../common/Icon";
import { severityLabel } from "../../utils/severity";
import { formatINR } from "../../utils/formatters";

export default function DecisionPack({ projectData }) {
  const decisions = projectData.controls_brief?.decisions || [];

  if (!decisions || decisions.length === 0) {
    return (
      <section className="decision-pack">
        <div className="pack-header">
          <h2>Today's Decisions</h2>
          <p>No active decisions at this time.</p>
        </div>
      </section>
    );
  }

  const recoveryPotential = projectData.controls_brief?.schedule_exposure_days
    ? Math.max(1, Math.round(projectData.controls_brief.schedule_exposure_days * 0.4))
    : 0;

  const costExposure = projectData.controls_brief?.schedule_exposure_days
    ? projectData.controls_brief.schedule_exposure_days * (projectData.controls_brief.daily_delay_cost || 0)
    : 0;

  return (
    <section className="decision-pack">
      <div className="pack-header">
        <h2>Today's Decisions</h2>
        <p>Actions required to maintain schedule and mitigate risk</p>
      </div>
      <div className="decision-cards">
        {decisions.map((decision, idx) => (
          <article key={idx} className="decision-card-exec">
            <div className="card-header">
              <h3>{decision.title}</h3>
              <span className={`priority-badge priority-${decision.priority}`}>
                {severityLabel(decision.priority)}
              </span>
            </div>
            <p className="card-reason">{decision.rationale}</p>
            <div className="card-metadata">
              <div className="meta-item">
                <span>👤 Owner</span>
                <strong>{decision.owner}</strong>
              </div>
              <div className="meta-item">
                <span>📅 Due</span>
                <strong>{decision.due}</strong>
              </div>
              <div className="meta-item">
                <span>⚡ Impact</span>
                <strong>{`Recover ${recoveryPotential} day${recoveryPotential === 1 ? "" : "s"}`}</strong>
              </div>
            </div>
            <div className="card-metadata card-metadata-compact">
              <div className="meta-item">
                <span>Estimated Cost Exposure</span>
                <strong>{costExposure ? formatINR(costExposure) : '₹0'}</strong>
                <small style={{display:'block', marginTop:3, color:'#8a9aaa', fontSize:10, fontWeight:400, letterSpacing:0, textTransform:'none'}}>Modeled estimate: delay days × assumed daily cost rate</small>
              </div>
              <div className="meta-item">
                <span>Delay rate</span>
                <strong>{projectData.controls_brief?.daily_delay_cost ? `${formatINR(projectData.controls_brief.daily_delay_cost)}/day` : 'N/A'}</strong>
              </div>
            </div>
            {decision.target && (
              <div className="card-target">
                <span>Target Action</span>
                <strong>{decision.target}</strong>
              </div>
            )}
            <div className="card-actions">
              <button type="button" disabled>Assign</button>
              <button type="button" disabled>Mark Complete</button>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}
