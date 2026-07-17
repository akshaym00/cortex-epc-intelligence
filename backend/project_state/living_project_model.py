"""
Living Project Model.

Represents the current state of the project.
"""

from datetime import datetime, timezone
from pydantic import Field

from backend.models.base import CortexBaseModel
from backend.models.project import Project
from backend.project_state.entity_state import EntityState
from typing import Any

from backend.models.event import ProjectEvent


class LivingProjectModel(CortexBaseModel):
    """
    Digital Twin of the current project.
    """

    project: Project

    # entity_id -> EntityState
    state_index: dict[str, EntityState] = Field(default_factory=dict)

    metadata: dict[str, Any] = Field(
    default_factory=dict
)

    history: list[ProjectEvent] = Field(
        default_factory=list
    )

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))