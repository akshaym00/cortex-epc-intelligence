"""
Project event model.

Represents a significant change detected from
project documents.
"""

from pydantic import Field

from backend.models.base import CortexBaseModel


class ProjectEvent(CortexBaseModel):
    """
    Represents an event detected in a project.
    """

    title: str

    event_type: str

    description: str

    affected_entity_name: str

    severity: str = "medium"

    confidence: float = 1.0

    metadata: dict = Field(default_factory=dict)