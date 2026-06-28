"""
Project model for Project Cortex.

A Project is the top-level container for the Living Project Model.
It stores all entities and relationships that describe a project.
"""

from pydantic import Field

from backend.models.base import CortexBaseModel
from backend.models.entity import Entity
from backend.models.relationship import Relationship


class Project(CortexBaseModel):
    """
    Represents a project and all knowledge associated with it.
    """

    # Project name
    name: str

    # Optional description
    description: str | None = None

    # Current project status
    status: str = "active"

    # All entities belonging to this project
    entities: list[Entity] = Field(default_factory=list)

    # Relationships between entities
    relationships: list[Relationship] = Field(default_factory=list)