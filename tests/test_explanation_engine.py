from backend.models.entity import Entity
from backend.models.enums import EntityType
from backend.models.project import Project
from backend.reasoning.explanation_engine import ExplanationEngine


def test_explain_path():

    generator = Entity(
        entity_type=EntityType.EQUIPMENT,
        name="Generator",
    )

    installation = Entity(
        entity_type=EntityType.TASK,
        name="Installation",
    )

    project = Project(
        name="Demo",
        entities=[
            generator,
            installation,
        ],
    )

    engine = ExplanationEngine()

    explanation = engine.explain_path(
        project,
        [
            generator.id,
            installation.id,
        ],
    )

    assert explanation == "Generator → Installation"