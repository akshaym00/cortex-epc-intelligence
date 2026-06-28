"""
Pipeline result model.
"""

from pydantic import BaseModel

from backend.models.entity import Entity
from backend.models.event import ProjectEvent
from backend.models.project import Project
from backend.models.relationship import Relationship


class PipelineResult(BaseModel):
    """
    Result returned by the Project Cortex analysis pipeline.
    """

    document_text: str

    entities: list[Entity]

    relationships: list[Relationship]

    events: list[ProjectEvent]

    project: Project

    model_config = {
        "arbitrary_types_allowed": True,
    }