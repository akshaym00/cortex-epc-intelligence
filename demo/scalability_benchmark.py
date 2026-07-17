"""Repeatable core graph benchmark for the hackathon scalability claim."""

from time import perf_counter

from backend.graph.graph_builder import GraphBuilder
from backend.models.entity import Entity
from backend.models.enums import EntityType, RelationshipType
from backend.models.project import Project
from backend.models.relationship import Relationship
from backend.reasoning.dependency_reasoner import DependencyReasoner


CONTRACTOR_COUNT = 200
LINE_ITEM_COUNT = 15_000


def run_benchmark() -> dict:
    started = perf_counter()
    contractors = [
        Entity(entity_type=EntityType.CONTRACTOR, name=f"Contractor {index:03d}")
        for index in range(CONTRACTOR_COUNT)
    ]
    activities = [
        Entity(entity_type=EntityType.TASK, name=f"Schedule Activity {index:05d}")
        for index in range(LINE_ITEM_COUNT)
    ]
    relationships = []

    for index, activity in enumerate(activities):
        relationships.append(
            Relationship(
                source_entity_id=contractors[index % CONTRACTOR_COUNT].id,
                target_entity_id=activity.id,
                relationship_type=RelationshipType.OWNED_BY,
            )
        )
        if index > 0:
            relationships.append(
                Relationship(
                    source_entity_id=activities[index - 1].id,
                    target_entity_id=activity.id,
                    relationship_type=RelationshipType.DEPENDS_ON,
                )
            )

    model_seconds = perf_counter() - started
    graph_started = perf_counter()
    graph = GraphBuilder().build(
        Project(
            name="Synthetic 15K-line EPC project",
            entities=[*contractors, *activities],
            relationships=relationships,
        )
    )
    graph_seconds = perf_counter() - graph_started
    traversal_started = perf_counter()
    downstream = DependencyReasoner().get_downstream_entities(
        graph,
        activities[0].id,
    )
    traversal_seconds = perf_counter() - traversal_started

    return {
        "entities": graph.number_of_nodes(),
        "relationships": graph.number_of_edges(),
        "downstream_entities": len(downstream),
        "model_seconds": round(model_seconds, 3),
        "graph_seconds": round(graph_seconds, 3),
        "traversal_seconds": round(traversal_seconds, 3),
    }


if __name__ == "__main__":
    result = run_benchmark()
    print("Project Cortex scalability benchmark")
    for key, value in result.items():
        print(f"{key}: {value}")
