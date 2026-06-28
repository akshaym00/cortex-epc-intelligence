"""
Relationship model for Project Cortex.

A Relationship connects two entities inside the Living Project Model.

Example:
    Cummins
        ── SUPPLIES ──► Generator G-12

    Generator G-12
        ── REQUIRES ──► Electrical Testing
"""

from typing import Any

from pydantic import Field

from backend.models.base import CortexBaseModel
from backend.models.enums import RelationshipType


class Relationship(CortexBaseModel):
    """
    Represents a connection between two entities.

    Relationships form the edges of the Living Project Graph.
    """

    # ID of the source entity
    source_entity_id: str

    # Type of relationship
    relationship_type: RelationshipType

    # ID of the destination entity
    target_entity_id: str

    # Optional human-readable description
    description: str | None = None

    # Flexible attributes for future extensions
    attributes: dict[str, Any] = Field(default_factory=dict)