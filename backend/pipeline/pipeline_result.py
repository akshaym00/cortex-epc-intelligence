"""
Pipeline result model.
"""

from pydantic import BaseModel

from backend.models.entity import Entity
from backend.models.project import Project


class PipelineResult(BaseModel):
    """
    Result returned by the analysis pipeline.
    """

    document_text: str

    entities: list[Entity]

    project: Project

    model_config = {
        "arbitrary_types_allowed": True,
    }