"""
Relationship extraction engine.

Uses the LLM to identify relationships between entities
mentioned in project documents.
"""

from backend.ai.llm_client import LLMClient
from backend.extraction.relationship_parser import RelationshipParser
from backend.models.enums import RelationshipType
from backend.models.relationship import Relationship
from backend.prompts.extraction_prompts import ExtractionPrompts


class RelationshipExtractor:
    """
    Extracts relationships from project documents.
    """

    def __init__(self):

        self.client = LLMClient()

    def extract(
        self,
        document: str,
        entity_lookup: dict[str, str],
        entity_type_lookup: dict[str, str] | None = None,
    ) -> list[Relationship]:
        """
        Extract relationships from the supplied document.

        Parameters
        ----------
        document
            Raw project document text.

        entity_lookup
            Maps entity names to entity IDs.

        Returns
        -------
        list[Relationship]
        """

        prompt = ExtractionPrompts.relationship_extraction(
            document,
            list(entity_lookup),
        )

        response = self.client.generate(prompt)

        parsed = RelationshipParser.parse(response)

        relationships: list[Relationship] = []
        entity_type_lookup = entity_type_lookup or {}

        # Separate LLM calls can vary capitalization or surrounding
        # whitespace for the same entity name. Resolve those harmless
        # differences instead of silently dropping the relationship.
        normalized_entity_lookup = {
            name.strip().casefold(): entity_id
            for name, entity_id in entity_lookup.items()
        }

        for item in parsed.relationships:

            source_id = normalized_entity_lookup.get(
                item.source.strip().casefold()
            )

            target_id = normalized_entity_lookup.get(
                item.target.strip().casefold()
            )

            if source_id is None or target_id is None:
                continue

            relationship_type = RelationshipType(
                item.relationship_type
            )

            if (
                relationship_type == RelationshipType.SUPPLIES
                and entity_type_lookup
            ):
                source_type = entity_type_lookup.get(source_id)
                supplier_ids = [
                    entity_id
                    for entity_id, entity_type in entity_type_lookup.items()
                    if entity_type in {"vendor", "contractor"}
                ]

                # LLMs occasionally attach "supplies" to a delivery
                # milestone. When the document has one unambiguous supplier,
                # repair the subject while preserving the supplied target.
                if source_type not in {"vendor", "contractor"}:
                    if len(supplier_ids) == 1:
                        source_id = supplier_ids[0]
                    else:
                        continue

            # Reverse dependency edges so impact flows correctly
            if relationship_type == RelationshipType.DEPENDS_ON:
                source_id, target_id = (
                    target_id,
                    source_id,
                )

            relationships.append(
                Relationship(
                    source_entity_id=source_id,
                    relationship_type=relationship_type,
                    target_entity_id=target_id,
                )
            )

        return relationships
