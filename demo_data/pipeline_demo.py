"""
Project Cortex Demonstration

Runs the complete analysis pipeline and prints
the extracted project knowledge.
"""

from backend.pipeline.analysis_pipeline import AnalysisPipeline


def print_separator(title: str) -> None:
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def main():

    pipeline = AnalysisPipeline()

    result = pipeline.analyze(
        "demo_data/sample_document.txt"
    )

    print_separator("PROJECT CORTEX")

    print("\nDocument Analyzed\n")

    print(result.document_text)

    print_separator("ENTITIES")

    if result.entities:

        for entity in result.entities:

            print(
                f"[{entity.entity_type.value.upper():12}] "
                f"{entity.name}"
            )

    else:

        print("No entities detected.")

    print_separator("RELATIONSHIPS")

    if result.relationships:

        entity_lookup = {
            entity.id: entity.name
            for entity in result.entities
        }

        for relationship in result.relationships:

            source = entity_lookup.get(
                relationship.source_entity_id,
                relationship.source_entity_id,
            )

            target = entity_lookup.get(
                relationship.target_entity_id,
                relationship.target_entity_id,
            )

            print(
                f"{source}"
            )
            print(
                f"    │"
            )
            print(
                f"    └── {relationship.relationship_type.value.upper()}"
            )
            print(
                f"            ▼"
            )
            print(
                f"{target}\n"
            )

    else:

        print("No relationships detected.")

    print_separator("EVENTS")

    if result.events:

        for event in result.events:

            print(f"Title       : {event.title}")

            print(f"Type        : {event.event_type}")

            print(
                f"Affected    : {event.affected_entity_name}"
            )

            print(
                f"Severity    : {event.severity}"
            )

            print(
                f"Description : {event.description}"
            )

            print("-" * 70)

    else:

        print("No events detected.")

    print_separator("GRAPH")

    graph = result.project.metadata["graph"]

    print(
        f"Nodes : {graph.number_of_nodes()}"
    )

    print(
        f"Edges : {graph.number_of_edges()}"
    )

    print_separator("SUMMARY")

    print(
        f"Entities Extracted      : {len(result.entities)}"
    )

    print(
        f"Relationships Extracted : {len(result.relationships)}"
    )

    print(
        f"Events Extracted        : {len(result.events)}"
    )

    print("\nSprint 3 Complete ✅")


if __name__ == "__main__":

    main()