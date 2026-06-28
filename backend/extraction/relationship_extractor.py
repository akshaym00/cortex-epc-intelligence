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
            document
        )

        response = self.client.generate(prompt)

        parsed = RelationshipParser.parse(response)

        relationships: list[Relationship] = []

        for item in parsed.relationships:

            source_id = entity_lookup.get(item.source)

            target_id = entity_lookup.get(item.target)

            if source_id is None or target_id is None:
                continue

            relationships.append(
                Relationship(
                    source_entity_id=source_id,
                    relationship_type=RelationshipType(
                        item.relationship_type
                    ),
                    target_entity_id=target_id,
                )
            )

        return relationships