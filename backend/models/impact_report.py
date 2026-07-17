"""
Impact Report model.
"""

from pydantic import Field

from backend.models.base import CortexBaseModel
from backend.models.impact import Impact


class ImpactReport(CortexBaseModel):
    """
    Complete impact analysis for one project event.
    """

    event_title: str

    impacted_entities: list[Impact] = Field(
        default_factory=list
    )

    summary: str = ""

    overall_severity: str = "low"

    delay_days: int = 0
    projected_completion_impact_days: int = 0
    methodology: str = ""
