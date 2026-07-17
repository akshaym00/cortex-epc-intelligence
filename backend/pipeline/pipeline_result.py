"""
Pipeline result model.
"""

from pydantic import BaseModel
from backend.models.recommendation import Recommendation

from backend.models.entity import Entity
from backend.models.event import ProjectEvent
from backend.models.project import Project
from backend.models.relationship import Relationship
import networkx as nx

from pydantic import BaseModel, Field

from backend.models.impact_report import ImpactReport
from backend.models.compliance import ComplianceFinding
from backend.models.controls import ProjectControlsBrief
from backend.project_state.living_project_model import (
    LivingProjectModel,
)


class PipelineResult(BaseModel):
    """
    Result returned by the Project Cortex analysis pipeline.
    """

    document_text: str

    entities: list[Entity]

    relationships: list[Relationship]

    events: list[ProjectEvent]

    project: Project

    living_project: LivingProjectModel | None = None
    graph: nx.DiGraph | None = None

    impact_reports: list[ImpactReport] = Field(
        default_factory=list
    )
    recommendations: list[Recommendation] = Field(
        default_factory=list
    )

    compliance_findings: list[ComplianceFinding] = Field(
        default_factory=list
    )

    controls_brief: ProjectControlsBrief | None = None

    model_config = {
        "arbitrary_types_allowed": True,
    }
