"""Run and record the verified 20-line RFI stress-test result."""

import json
from pathlib import Path
from time import perf_counter

from backend.pipeline.analysis_pipeline import AnalysisPipeline


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "demo" / "sample_documents" / "dense_rfi_log.txt"
OUTPUT = ROOT / "frontend" / "public" / "verified_dense_result.json"


def run():
    started = perf_counter()
    result = AnalysisPipeline().analyze(str(SOURCE))
    names = {entity.id: entity.name for entity in result.entities}
    reports = {report.event_title: report for report in result.impact_reports}

    payload = {
        "entities": [
            {
                "name": entity.name,
                "entity_type": entity.entity_type.value,
                "description": entity.description,
            }
            for entity in result.entities
        ],
        "relationships": [
            {
                "source": names.get(edge.source_entity_id, edge.source_entity_id),
                "relationship_type": edge.relationship_type.value,
                "target": names.get(edge.target_entity_id, edge.target_entity_id),
            }
            for edge in result.relationships
        ],
        "events": [
            {
                "title": event.title,
                "event_type": event.event_type,
                "description": event.description,
                "severity": event.severity,
                "reported_by": next(
                    (
                        entity.name for entity in result.entities
                        if entity.entity_type.value in {"vendor", "contractor"}
                        and entity.name.casefold() in event.description.casefold()
                    ),
                    None,
                ),
                "affected_entities": [
                    impact.affected_entity_name
                    for impact in reports.get(event.title, []).impacted_entities
                ] if event.title in reports else [],
            }
            for event in result.events
        ],
        "impacts": [
            {
                "event_title": report.event_title,
                "summary": report.summary,
                "overall_severity": report.overall_severity,
                "delay_days": report.delay_days,
                "projected_completion_impact_days": report.projected_completion_impact_days,
                "methodology": report.methodology,
                "impacted_entities": [
                    {
                        "name": impact.affected_entity_name,
                        "severity": impact.severity.value,
                        "reason": impact.reason,
                        "dependency_path": [names.get(item, item) for item in impact.dependency_path],
                        "delay_days": impact.delay_days,
                        "baseline_start": impact.baseline_start,
                        "baseline_finish": impact.baseline_finish,
                        "forecast_start": impact.forecast_start,
                        "forecast_finish": impact.forecast_finish,
                        "critical_path": impact.critical_path,
                    }
                    for impact in report.impacted_entities
                ],
            }
            for report in result.impact_reports
        ],
        "recommendations": [
            {
                "title": recommendation.title,
                "description": recommendation.description,
                "priority": recommendation.priority,
                "related_event": recommendation.related_event,
            }
            for recommendation in result.recommendations
        ],
        "compliance_findings": [finding.model_dump(mode="json") for finding in result.compliance_findings],
        "verification": {
            "source": "20-line synthetic RFI log",
            "elapsed_seconds": round(perf_counter() - started, 2),
            "raw_orphan_nodes": sum(
                1 for node in result.graph.nodes if result.graph.degree(node) == 0
            ),
        },
    }
    OUTPUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload["verification"]))


if __name__ == "__main__":
    run()
