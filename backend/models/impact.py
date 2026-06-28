"""
Impact model for Project Cortex.

Represents the downstream impact caused by a change
to an entity inside the Living Project Model.
"""

from pydantic import Field

from backend.models.base import CortexBaseModel
from backend.models.enums import ImpactSeverity


class Impact(CortexBaseModel):
    """
    Represents the impact of an event or change
    on another entity in the project.
    """

    # Entity affected
    affected_entity_id: str

    # Human-readable name
    affected_entity_name: str

    # How severe is the impact?
    severity: ImpactSeverity

    # Ordered dependency path
    dependency_path: list[str] = Field(default_factory=list)

    # Human-readable explanation
    reason: str

    # Optional confidence score
    confidence: float = 1.0