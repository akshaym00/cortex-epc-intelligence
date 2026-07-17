"""
Demo script for the Project Cortex analysis pipeline.

Runs the full pipeline on the sample document and prints
the analysis results.

Usage:
    python -m demo.demo_pipeline
"""

from pathlib import Path

from backend.pipeline.analysis_pipeline import AnalysisPipeline


def main():
    """Run the analysis pipeline on the sample document."""

    sample_path = (
        Path(__file__).resolve().parent / "sample_documents"
    )

    # Find the first .txt file in sample_documents, or fall back
    # to the demo_data sample
    txt_files = list(sample_path.glob("*.txt")) if sample_path.exists() else []

    if txt_files:
        document_path = str(txt_files[0])
    else:
        document_path = str(
            Path(__file__).resolve().parents[1]
            / "demo_data"
            / "sample_document.txt"
        )

    print(f"Analyzing: {document_path}")
    print("=" * 60)

    pipeline = AnalysisPipeline()
    result = pipeline.analyze(document_path)

    # --- Entities ---
    print(f"\nEntities ({len(result.entities)}):")
    print("-" * 40)

    for entity in result.entities:
        print(f"  [{entity.entity_type.value}] {entity.name}")

    # --- Relationships ---
    print(f"\nRelationships ({len(result.relationships)}):")
    print("-" * 40)

    entity_lookup = {
        entity.id: entity.name
        for entity in result.entities
    }

    for rel in result.relationships:
        source = entity_lookup.get(
            rel.source_entity_id,
            rel.source_entity_id,
        )
        target = entity_lookup.get(
            rel.target_entity_id,
            rel.target_entity_id,
        )
        print(f"  {source} --[{rel.relationship_type.value}]--> {target}")

    # --- Events ---
    print(f"\nEvents ({len(result.events)}):")
    print("-" * 40)

    for event in result.events:
        print(f"  [{event.severity}] {event.title}")
        print(f"         {event.description}")

    # --- Impact Reports ---
    print(f"\nImpact Reports ({len(result.impact_reports)}):")
    print("-" * 40)

    for report in result.impact_reports:
        print(f"  Event: {report.event_title}")
        print(f"  Severity: {report.overall_severity}")
        print(f"  Summary: {report.summary}")

        for impact in report.impacted_entities:
            print(f"    → {impact.affected_entity_name} ({impact.severity.value})")

    # --- Recommendations ---
    print(f"\nRecommendations ({len(result.recommendations)}):")
    print("-" * 40)

    for rec in result.recommendations:
        print(f"  [{rec.priority}] {rec.title}")
        print(f"         {rec.description}")

    # --- Controls Brief ---
    if result.controls_brief:
        brief = result.controls_brief
        print(f"\nProject Controls Brief:")
        print("-" * 40)
        print(f"  Gate Status: {brief.gate_status}")
        print(f"  Reason: {brief.status_reason}")
        print(f"  Schedule Exposure: {brief.schedule_exposure_days} days")
        print(f"  Confidence: {brief.confidence}%")

    print("\n" + "=" * 60)
    print("Analysis complete.")


if __name__ == "__main__":
    main()
