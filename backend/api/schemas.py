"""
API response schemas for Project Cortex.
"""

from pydantic import BaseModel


class EntityResponse(BaseModel):
    id: str
    name: str
    entity_type: str
    description: str | None = None


class RelationshipResponse(BaseModel):
    source: str
    source_entity_id: str | None = None
    relationship_type: str
    target: str
    target_entity_id: str | None = None


class EventResponse(BaseModel):
    title: str
    event_type: str
    description: str
    severity: str
    reported_by: str | None = None
    affected_entities: list[str] = []


class ImpactedEntityResponse(BaseModel):
    name: str
    severity: str
    reason: str
    dependency_path: list[str]
    delay_days: int
    baseline_start: str | None
    baseline_finish: str | None
    forecast_start: str | None
    forecast_finish: str | None
    critical_path: bool


class ImpactResponse(BaseModel):
    event_title: str
    summary: str
    overall_severity: str
    impacted_entities: list[ImpactedEntityResponse]
    delay_days: int
    projected_completion_impact_days: int
    methodology: str


class RecommendationResponse(BaseModel):
    title: str
    description: str
    priority: str
    related_event: str | None = None


class ComplianceFindingResponse(BaseModel):
    parameter: str
    required_value: float
    submitted_value: float
    unit: str
    deviation: float
    status: str
    requirement_citation: str
    submittal_citation: str
    recommendation: str


class ControlDecisionResponse(BaseModel):
    title: str
    owner: str
    priority: str
    due: str
    rationale: str
    target: str | None = None


class ConfidenceBreakdownResponse(BaseModel):
    extraction_certainty: int
    dependency_completeness: int
    weight_extraction: float
    weight_dependency: float
    base_confidence: int
    final_confidence: int

class ProjectControlsBriefResponse(BaseModel):
    gate_status: str
    status_reason: str
    procurement_gate: str
    schedule_exposure_days: int
    recoverable_days: int
    commercial_notice: str
    confidence: int
    extraction_certainty: int
    dependency_completeness: int
    confidence_breakdown: ConfidenceBreakdownResponse
    daily_delay_cost: int
    impacted_entities: list[str]
    critical_path: list[str]
    blocked_gates: list[str]
    next_72_hours: list[str]
    decisions: list[ControlDecisionResponse]


class AnalyzeResponse(BaseModel):
    """
    Response returned by the /analyze endpoint.
    """

    entities: list[EntityResponse]

    relationships: list[RelationshipResponse]

    events: list[EventResponse]

    impacts: list[ImpactResponse]

    recommendations: list[RecommendationResponse]

    compliance_findings: list[ComplianceFindingResponse]

    controls_brief: ProjectControlsBriefResponse | None = None
