"""
Project analysis pipeline.

Coordinates the complete document analysis workflow.
"""

from backend.extraction.entity_extractor import EntityExtractor
from backend.extraction.event_extractor import EventExtractor
from backend.extraction.relationship_extractor import RelationshipExtractor
from backend.graph.graph_builder import GraphBuilder
from backend.ingestion.loader_factory import LoaderFactory
from backend.models.project import Project
from backend.pipeline.pipeline_result import PipelineResult


class AnalysisPipeline:
    """
    High-level orchestration service.
    """

    def __init__(self):

        self.entity_extractor = EntityExtractor()

        self.relationship_extractor = RelationshipExtractor()

        self.event_extractor = EventExtractor()

        self.graph_builder = GraphBuilder()

    def analyze(
        self,
        file_path: str,
    ) -> PipelineResult:

        loader = LoaderFactory.create(file_path)

        document_text = loader.load(file_path)

        # -----------------------------
        # Extract entities
        # -----------------------------
        entities = self.entity_extractor.extract(
            document_text
        )

        entity_lookup = {
            entity.name: entity.id
            for entity in entities
        }

        # -----------------------------
        # Extract relationships
        # -----------------------------
        relationships = (
            self.relationship_extractor.extract(
                document_text,
                entity_lookup,
            )
        )

        # -----------------------------
        # Extract events
        # -----------------------------
        events = self.event_extractor.extract(
            document_text
        )

        # -----------------------------
        # Build project
        # -----------------------------
        project = Project(
            name="Auto Generated Project",
            entities=entities,
            relationships=relationships,
        )

        graph = self.graph_builder.build(project)

        project.metadata["graph"] = graph

        project.metadata["events"] = events

        return PipelineResult(
            document_text=document_text,
            entities=entities,
            relationships=relationships,
            events=events,
            project=project,
        )