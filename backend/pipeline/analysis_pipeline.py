"""
Project analysis pipeline.

Coordinates the complete document analysis workflow.
"""

from difflib import SequenceMatcher
from concurrent.futures import ThreadPoolExecutor

from backend.extraction.entity_extractor import EntityExtractor
from backend.extraction.event_extractor import EventExtractor
from backend.extraction.relationship_extractor import RelationshipExtractor
from backend.graph.graph_builder import GraphBuilder
from backend.ingestion.loader_factory import LoaderFactory
from backend.models.project import Project
from backend.pipeline.pipeline_result import PipelineResult
from backend.project_state.living_project_factory import (
    LivingProjectFactory,
)
from backend.project_state.state_updater import StateUpdater
from backend.reasoning.impact_engine import ImpactEngine
from backend.reasoning.project_controls_brief import ProjectControlsBriefGenerator
from backend.reasoning.spec_compliance import SpecComplianceAnalyzer
from backend.recommendation.recommendation_engine import (
    RecommendationEngine,
)


class AnalysisPipeline:
    """
    High-level orchestration service.
    """

    def __init__(self):

        self.entity_extractor = EntityExtractor()

        self.relationship_extractor = RelationshipExtractor()

        self.event_extractor = EventExtractor()

        self.graph_builder = GraphBuilder()

        # Project State
        self.state_updater = StateUpdater()

        # Reasoning
        self.impact_engine = ImpactEngine()
        self.spec_compliance = SpecComplianceAnalyzer()
        self.controls_brief_generator = ProjectControlsBriefGenerator()

        # Recommendations
        self.recommendation_engine = RecommendationEngine()

    def analyze(
        self,
        file_path: str,
    ) -> PipelineResult:

        loader = LoaderFactory.create(file_path)

        document_text = loader.load(file_path)
        compliance_findings = self.spec_compliance.analyze(document_text)

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

        # Relationship and event extraction both depend on the entity list,
        # but not on each other. Run them concurrently to reduce document
        # analysis latency without changing results.
        with ThreadPoolExecutor(max_workers=2) as executor:
            relationships_future = executor.submit(
                self.relationship_extractor.extract,
                document_text,
                entity_lookup,
                {
                    entity.id: entity.entity_type.value
                    for entity in entities
                },
            )
            events_future = executor.submit(
                self.event_extractor.extract,
                document_text,
                [entity.name for entity in entities],
            )
            relationships = relationships_future.result()
            events = events_future.result()

        # Event/issue/risk entities that restate timeline occurrences create
        # disconnected duplicate nodes. Keep the event as the occurrence and
        # persistent entities as the graph model.
        duplicate_entity_ids = {
            entity.id
            for entity in entities
            if entity.entity_type.value in {"event", "issue", "risk"}
            and any(
                SequenceMatcher(
                    None,
                    entity.name.casefold(),
                    event.title.casefold(),
                ).ratio() >= 0.55
                or entity.name.casefold() in event.description.casefold()
                for event in events
            )
        }

        if duplicate_entity_ids:
            entities = [
                entity for entity in entities
                if entity.id not in duplicate_entity_ids
            ]
            relationships = [
                relationship for relationship in relationships
                if relationship.source_entity_id not in duplicate_entity_ids
                and relationship.target_entity_id not in duplicate_entity_ids
            ]

        # -----------------------------
        # Build Project
        # -----------------------------

        project = Project(
            name="Auto Generated Project",
            entities=entities,
            relationships=relationships,
        )

        # -----------------------------
        # Build Graph
        # -----------------------------

        graph = self.graph_builder.build(project)

        project.metadata["graph"] = graph
        project.metadata["events"] = events

        # -----------------------------
        # Create Living Project Model
        # -----------------------------

        living_project = LivingProjectFactory.create(
            project
        )

        # -----------------------------
        # Update project state
        # -----------------------------

        impact_reports = []

        for event in events:

            living_project = self.state_updater.update(
                living_project,
                event,
            )

            impact_report = self.impact_engine.analyze(
                living_project,
                graph,
                event,
            )

            impact_reports.append(
                impact_report
            )

        # -----------------------------
        # Generate Recommendations
        # -----------------------------

        recommendations = (
            self.recommendation_engine.generate(
                events,
                impact_reports,
            )
        )

        controls_brief = self.controls_brief_generator.generate(
            project,
            impact_reports,
            recommendations,
            compliance_findings,
        )

        # -----------------------------
        # Return Result
        # -----------------------------

        return PipelineResult(
            document_text=document_text,
            entities=entities,
            relationships=relationships,
            events=events,
            project=project,
            living_project=living_project,
            graph=graph,
            impact_reports=impact_reports,
            recommendations=recommendations,
            compliance_findings=compliance_findings,
            controls_brief=controls_brief,
        )
