"""
API routes for Project Cortex.
"""

import os
import tempfile
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from backend.api.schemas import (
    AnalyzeResponse,
    EntityResponse,
    RelationshipResponse,
    EventResponse,
    ImpactResponse,
    ImpactedEntityResponse,
    RecommendationResponse,
    ComplianceFindingResponse,
    ConfidenceBreakdownResponse,
    ControlDecisionResponse,
    ProjectControlsBriefResponse,
)

from backend.pipeline.analysis_pipeline import AnalysisPipeline
from backend.pipeline.pipeline_result import PipelineResult

router = APIRouter()

pipeline = AnalysisPipeline()

# ---------------------------------------------------------------------------
# Demo document registry
# ---------------------------------------------------------------------------

_DEMO_DOCS_DIR = Path(__file__).resolve().parents[2] / "demo" / "sample_documents"

_DEMO_SCENARIOS = {
    "rfi": _DEMO_DOCS_DIR / "vendor_delay.txt",
    "compliance": _DEMO_DOCS_DIR / "spec_compliance_case.txt",
}


# ---------------------------------------------------------------------------
# Shared serialization helper
# ---------------------------------------------------------------------------

def _build_response(result: PipelineResult) -> AnalyzeResponse:
    """Convert a PipelineResult into the API response schema."""

    entity_lookup = {entity.id: entity.name for entity in result.entities}

    return AnalyzeResponse(

        entities=[
            EntityResponse(
                id=entity.id,
                name=entity.name,
                entity_type=entity.entity_type.value,
                description=entity.description,
            )
            for entity in result.entities
        ],

        relationships=[
            RelationshipResponse(
                source=entity_lookup.get(
                    relationship.source_entity_id,
                    relationship.source_entity_id,
                ),
                source_entity_id=relationship.source_entity_id,
                relationship_type=relationship.relationship_type.value,
                target=entity_lookup.get(
                    relationship.target_entity_id,
                    relationship.target_entity_id,
                ),
                target_entity_id=relationship.target_entity_id,
            )
            for relationship in result.relationships
        ],

        events=[
            EventResponse(
                title=event.title,
                event_type=event.event_type,
                description=event.description,
                severity=event.severity,
                reported_by=next(
                    (
                        entity.name
                        for entity in result.entities
                        if entity.entity_type.value in {"vendor", "contractor"}
                        and entity.name.casefold() in event.description.casefold()
                    ),
                    None,
                ),
                affected_entities=next(
                    (
                        [
                            impact.affected_entity_name
                            for impact in report.impacted_entities
                        ]
                        for report in result.impact_reports
                        if report.event_title == event.title
                    ),
                    [],
                ),
            )
            for event in result.events
        ],

        impacts=[
            ImpactResponse(
                event_title=report.event_title,
                summary=report.summary,
                overall_severity=report.overall_severity,
                impacted_entities=[
                    ImpactedEntityResponse(
                        name=impact.affected_entity_name,
                        severity=impact.severity.value,
                        reason=impact.reason,
                        dependency_path=[
                            entity_lookup.get(entity_id, entity_id)
                            for entity_id in impact.dependency_path
                        ],
                        delay_days=impact.delay_days,
                        baseline_start=impact.baseline_start,
                        baseline_finish=impact.baseline_finish,
                        forecast_start=impact.forecast_start,
                        forecast_finish=impact.forecast_finish,
                        critical_path=impact.critical_path,
                    )
                    for impact in report.impacted_entities
                ],
                delay_days=report.delay_days,
                projected_completion_impact_days=(
                    report.projected_completion_impact_days
                ),
                methodology=report.methodology,
            )
            for report in result.impact_reports
        ],

        recommendations=[
            RecommendationResponse(
                title=recommendation.title,
                description=recommendation.description,
                priority=recommendation.priority,
                related_event=recommendation.related_event,
            )
            for recommendation in result.recommendations
        ],

        compliance_findings=[
            ComplianceFindingResponse(
                parameter=finding.parameter,
                required_value=finding.required_value,
                submitted_value=finding.submitted_value,
                unit=finding.unit,
                deviation=finding.deviation,
                status=finding.status,
                requirement_citation=finding.requirement_citation,
                submittal_citation=finding.submittal_citation,
                recommendation=finding.recommendation,
            )
            for finding in result.compliance_findings
        ],

        controls_brief=(
            ProjectControlsBriefResponse(
                gate_status=result.controls_brief.gate_status,
                status_reason=result.controls_brief.status_reason,
                procurement_gate=result.controls_brief.procurement_gate,
                schedule_exposure_days=(
                    result.controls_brief.schedule_exposure_days
                ),
                recoverable_days=result.controls_brief.recoverable_days,
                commercial_notice=result.controls_brief.commercial_notice,
                confidence=result.controls_brief.confidence,
                extraction_certainty=result.controls_brief.extraction_certainty,
                dependency_completeness=result.controls_brief.dependency_completeness,
                confidence_breakdown=ConfidenceBreakdownResponse(
                    **result.controls_brief.confidence_breakdown
                ),
                daily_delay_cost=result.controls_brief.daily_delay_cost,
                impacted_entities=result.controls_brief.impacted_entities,
                critical_path=result.controls_brief.critical_path,
                blocked_gates=result.controls_brief.blocked_gates,
                next_72_hours=result.controls_brief.next_72_hours,
                decisions=[
                    ControlDecisionResponse(
                        title=decision.title,
                        owner=decision.owner,
                        priority=decision.priority,
                        due=decision.due,
                        rationale=decision.rationale,
                        target=decision.target,
                    )
                    for decision in result.controls_brief.decisions
                ],
            )
            if result.controls_brief
            else None
        ),
    )


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@router.get("/")
def root():
    return {"message": "Project Cortex API is running."}


@router.get("/health")
def health():
    return {"status": "healthy"}


@router.post(
    "/analyze",
    response_model=AnalyzeResponse,
)
async def analyze_document(
    file: UploadFile = File(...),
):
    """Analyze an uploaded project document through the full pipeline."""

    suffix = os.path.splitext(file.filename)[1]

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=suffix,
    ) as temp:
        temp.write(await file.read())
        temp_path = temp.name

    result = pipeline.analyze(temp_path)
    os.remove(temp_path)

    return _build_response(result)


@router.get(
    "/analyze/demo/{scenario}",
    response_model=AnalyzeResponse,
)
def analyze_demo_scenario(scenario: str):
    """
    Run the full analysis pipeline on a bundled demo document.

    Accepted scenario names:
      - ``rfi``        — Vendor delay / RFI scenario (vendor_delay.txt)
      - ``compliance`` — Specification compliance scenario (spec_compliance_case.txt)

    Behaves identically to uploading the document via POST /analyze.
    """

    doc_path = _DEMO_SCENARIOS.get(scenario.lower())

    if doc_path is None:
        raise HTTPException(
            status_code=404,
            detail=(
                f"Unknown demo scenario '{scenario}'. "
                f"Valid options: {list(_DEMO_SCENARIOS.keys())}"
            ),
        )

    if not doc_path.exists():
        raise HTTPException(
            status_code=500,
            detail=f"Demo document not found at expected path: {doc_path}",
        )

    result = pipeline.analyze(str(doc_path))

    return _build_response(result)
