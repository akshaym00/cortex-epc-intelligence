"""
RFI stress-test exercising all updated logic paths.

Runs the 20-line dense RFI log through the full pipeline and
prints every output layer: entities, relationships, events,
impacts (with schedule forecasts), recommendations, compliance,
and the controls brief (confidence breakdown, blocked gates,
cost exposure).

Exit code 1 on any sanity failure so CI can catch regressions.
"""

import io
import json
import sys
from pathlib import Path
from time import perf_counter

# Force UTF-8 output on Windows (cp1252 console cannot render box-drawing
# or Unicode arrows that appear in comments and section separators).
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

from backend.pipeline.analysis_pipeline import AnalysisPipeline

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "demo" / "sample_documents" / "dense_rfi_log.txt"

SEPARATOR = "=" * 72
THIN = "-" * 72


def sanity_check(label: str, condition: bool, detail: str = ""):
    tag = "  [PASS]" if condition else "  [FAIL]"
    msg = f"{tag}  {label}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def run():
    print(SEPARATOR)
    print("  PROJECT CORTEX -- 20-LINE RFI STRESS TEST")
    print(SEPARATOR)

    started = perf_counter()
    result = AnalysisPipeline().analyze(str(SOURCE))
    elapsed = round(perf_counter() - started, 2)

    names = {e.id: e.name for e in result.entities}
    all_ok = True

    # ── 1. Entities ──────────────────────────────────────────────
    print(f"\n[ENTITIES] ({len(result.entities)})")
    print(THIN)
    for e in result.entities:
        print(f"  [{e.entity_type.value:>12}]  {e.name}")

    all_ok &= sanity_check(
        "At least 10 entities extracted",
        len(result.entities) >= 10,
        f"got {len(result.entities)}",
    )

    # ── 2. Relationships ─────────────────────────────────────────
    print(f"\n[RELATIONSHIPS] ({len(result.relationships)})")
    print(THIN)
    for r in result.relationships:
        src = names.get(r.source_entity_id, r.source_entity_id)
        tgt = names.get(r.target_entity_id, r.target_entity_id)
        print(f"  {src}  --[{r.relationship_type.value}]-->  {tgt}")

    all_ok &= sanity_check(
        "At least 8 relationships extracted",
        len(result.relationships) >= 8,
        f"got {len(result.relationships)}",
    )

    # ── 3. Events ────────────────────────────────────────────────
    print(f"\n[EVENTS] ({len(result.events)})")
    print(THIN)
    for ev in result.events:
        print(f"  [{ev.severity:>8}]  {ev.title}")
        print(f"             {ev.description}")

    all_ok &= sanity_check(
        "At least 1 event extracted",
        len(result.events) >= 1,
        f"got {len(result.events)}",
    )

    # ── 4. Impact Reports ────────────────────────────────────────
    print(f"\n[IMPACT REPORTS] ({len(result.impact_reports)})")
    print(THIN)
    for report in result.impact_reports:
        print(f"  Event: {report.event_title}")
        print(f"    Overall severity : {report.overall_severity}")
        print(f"    Delay days       : {report.delay_days}")
        print(f"    Completion impact: {report.projected_completion_impact_days} days")
        print(f"    Methodology      : {report.methodology}")
        print(f"    Summary          : {report.summary}")

        for impact in report.impacted_entities:
            path_names = [names.get(n, n) for n in impact.dependency_path]
            print(f"      -> {impact.affected_entity_name}")
            print(f"        severity={impact.severity.value}  delay={impact.delay_days}d  critical={impact.critical_path}")
            print(f"        baseline: {impact.baseline_start} --> {impact.baseline_finish}")
            print(f"        forecast: {impact.forecast_start} --> {impact.forecast_finish}")
            print(f"        path: {' -> '.join(path_names)}")

        # Sanity: no negative delay
        all_ok &= sanity_check(
            f"  No negative delay ({report.event_title})",
            report.delay_days >= 0,
            f"delay_days={report.delay_days}",
        )
        all_ok &= sanity_check(
            f"  No negative completion impact ({report.event_title})",
            report.projected_completion_impact_days >= 0,
            f"completion_impact={report.projected_completion_impact_days}",
        )

    # ── 5. Recommendations ───────────────────────────────────────
    print(f"\n[RECOMMENDATIONS] ({len(result.recommendations)})")
    print(THIN)
    for rec in result.recommendations:
        print(f"  [{rec.priority:>6}]  {rec.title}")
        print(f"           {rec.description}")
        print(f"           related_event: {rec.related_event}")

    # ── 6. Compliance Findings ───────────────────────────────────
    print(f"\n[COMPLIANCE FINDINGS] ({len(result.compliance_findings)})")
    print(THIN)
    if result.compliance_findings:
        for f in result.compliance_findings:
            print(f"  {f.parameter}: required={f.required_value}{f.unit}, submitted={f.submitted_value}{f.unit}")
            print(f"    deviation={f.deviation}, status={f.status}")
            print(f"    recommendation: {f.recommendation}")
    else:
        print("  (none — RFI log has no spec requirement/submittal pairs)")

    # ── 7. Controls Brief ────────────────────────────────────────
    brief = result.controls_brief
    print(f"\n[PROJECT CONTROLS BRIEF]")
    print(THIN)
    if brief:
        print(f"  Gate Status          : {brief.gate_status}")
        print(f"  Status Reason        : {brief.status_reason}")
        print(f"  Procurement Gate     : {brief.procurement_gate}")
        print(f"  Schedule Exposure    : {brief.schedule_exposure_days} days")
        print(f"  Recoverable Days     : {brief.recoverable_days}")
        print(f"  Commercial Notice    : {brief.commercial_notice}")
        print(f"  Daily Delay Cost     : ${brief.daily_delay_cost:,}")
        print(f"  Confidence           : {brief.confidence}%")
        print(f"  Extraction Certainty : {brief.extraction_certainty}%")
        print(f"  Dep. Completeness    : {brief.dependency_completeness}%")

        bd = brief.confidence_breakdown
        print(f"\n  CONFIDENCE BREAKDOWN:")
        print(f"    extraction_certainty    = {bd.get('extraction_certainty', 'N/A')}%")
        print(f"    dependency_completeness = {bd.get('dependency_completeness', 'N/A')}%")
        print(f"    weight_extraction       = {bd.get('weight_extraction', 'N/A')}")
        print(f"    weight_dependency       = {bd.get('weight_dependency', 'N/A')}")
        print(f"    base_confidence         = {bd.get('base_confidence', 'N/A')}%")
        print(f"    final_confidence        = {bd.get('final_confidence', 'N/A')}%")

        print(f"\n  Impacted Entities    : {', '.join(brief.impacted_entities) or '(none)'}")
        print(f"  Critical Path        : {' -> '.join(brief.critical_path) or '(none)'}")
        print(f"  Blocked Gates        : {', '.join(brief.blocked_gates) or '(none)'}")
        print(f"  Next 72 Hours        :")
        for action in brief.next_72_hours:
            print(f"    * {action}")

        print(f"\n  DECISIONS ({len(brief.decisions)}):")
        for d in brief.decisions:
            print(f"    [{d.priority:>6}] {d.title}  (owner: {d.owner}, due: {d.due})")
            print(f"            rationale: {d.rationale}")
            if d.target:
                print(f"            target: {d.target}")

        # ── Controls Brief sanity checks ─────────────────────────
        print(f"\n{'- ' * 20}")
        print("CONTROLS BRIEF SANITY CHECKS:")

        all_ok &= sanity_check(
            "Gate status is a known value",
            brief.gate_status in {"CLEAR", "AT RISK", "ON HOLD"},
            f"got '{brief.gate_status}'",
        )
        all_ok &= sanity_check(
            "Schedule exposure >= 0",
            brief.schedule_exposure_days >= 0,
            f"got {brief.schedule_exposure_days}",
        )
        all_ok &= sanity_check(
            "Recoverable days >= 0",
            brief.recoverable_days >= 0,
            f"got {brief.recoverable_days}",
        )
        all_ok &= sanity_check(
            "Recoverable <= exposure",
            brief.recoverable_days <= brief.schedule_exposure_days,
            f"{brief.recoverable_days} <= {brief.schedule_exposure_days}",
        )
        all_ok &= sanity_check(
            "Daily delay cost >= 0",
            brief.daily_delay_cost >= 0,
            f"got ${brief.daily_delay_cost:,}",
        )
        all_ok &= sanity_check(
            "Daily delay cost not absurd (< $1M/day)",
            brief.daily_delay_cost < 1_000_000,
            f"got ${brief.daily_delay_cost:,}",
        )
        all_ok &= sanity_check(
            "Confidence 0-100%",
            0 <= brief.confidence <= 100,
            f"got {brief.confidence}%",
        )
        all_ok &= sanity_check(
            "Extraction certainty 0-100%",
            0 <= brief.extraction_certainty <= 100,
            f"got {brief.extraction_certainty}%",
        )
        all_ok &= sanity_check(
            "Dependency completeness 0-100%",
            0 <= brief.dependency_completeness <= 100,
            f"got {brief.dependency_completeness}%",
        )

        base = bd.get("base_confidence", -1)
        final = bd.get("final_confidence", -1)
        all_ok &= sanity_check(
            "Breakdown base_confidence 0-100%",
            0 <= base <= 100,
            f"got {base}%",
        )
        all_ok &= sanity_check(
            "Breakdown final_confidence 0-100%",
            0 <= final <= 100,
            f"got {final}%",
        )
        all_ok &= sanity_check(
            "Weights sum to ~1.0",
            abs(bd.get("weight_extraction", 0) + bd.get("weight_dependency", 0) - 1.0) < 0.01,
            f"got {bd.get('weight_extraction', 0) + bd.get('weight_dependency', 0)}",
        )

        total_cost_exposure = brief.daily_delay_cost * brief.schedule_exposure_days
        print(f"\n  TOTAL COST EXPOSURE: ${total_cost_exposure:,}")
        all_ok &= sanity_check(
            "Total cost exposure >= 0",
            total_cost_exposure >= 0,
            f"${total_cost_exposure:,}",
        )
    else:
        print("  [FAIL]  controls_brief is None!")
        all_ok = False

    # ── 8. Graph Stats ───────────────────────────────────────────
    print(f"\n[GRAPH STATS]")
    print(THIN)
    g = result.graph
    print(f"  Nodes: {g.number_of_nodes()}")
    print(f"  Edges: {g.number_of_edges()}")
    orphans = sum(1 for n in g.nodes if g.degree(n) == 0)
    print(f"  Orphan nodes: {orphans}")

    # ── Summary ──────────────────────────────────────────────────
    print(f"\n{SEPARATOR}")
    print(f"  Elapsed: {elapsed}s")
    if all_ok:
        print("  >>> ALL SANITY CHECKS PASSED <<<")
    else:
        print("  >>> SOME SANITY CHECKS FAILED -- review output above <<<")
    print(SEPARATOR)

    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    run()
