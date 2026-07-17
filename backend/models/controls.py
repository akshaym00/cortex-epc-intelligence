"""
Project controls decision models.
"""

from pydantic import Field

from backend.models.base import CortexBaseModel


class ControlDecision(CortexBaseModel):
    """
    Action a project manager or controls engineer can assign.
    """

    title: str
    owner: str
    priority: str
    due: str
    rationale: str
    target: str | None = None


class ProjectControlsBrief(CortexBaseModel):
    """
    Executive project-controls view generated from the reasoning layer.
    """

    gate_status: str = "CLEAR"
    status_reason: str = "No active blockers detected."
    procurement_gate: str = "Proceed"
    schedule_exposure_days: int = 0
    recoverable_days: int = 0
    commercial_notice: str = "No delay notice currently triggered."
    confidence: int = 80
    extraction_certainty: int = 0
    dependency_completeness: int = 0
    confidence_breakdown: dict[str, int | float] = Field(default_factory=dict)
    daily_delay_cost: int = 0
    impacted_entities: list[str] = Field(default_factory=list)
    critical_path: list[str] = Field(default_factory=list)
    blocked_gates: list[str] = Field(default_factory=list)
    next_72_hours: list[str] = Field(default_factory=list)
    decisions: list[ControlDecision] = Field(default_factory=list)
