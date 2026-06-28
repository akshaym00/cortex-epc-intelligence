"""
Entity extraction engine.
"""

from backend.ai.llm_client import LLMClient
from backend.extraction.parser import ExtractionParser
from backend.models.entity import Entity
from backend.models.enums import EntityType
from backend.prompts.extraction_prompts import ExtractionPrompts


class EntityExtractor:
    """
    Extracts project entities from text.
    """

    def __init__(self):
        self.client = LLMClient()

    def extract(self, document: str) -> list[Entity]:

        prompt = ExtractionPrompts.entity_extraction(document)

        response = self.client.generate(prompt)

        parsed = ExtractionParser.parse_entities(response)

        entities = []

        for item in parsed.entities:

            entities.append(
                Entity(
                    entity_type=EntityType(item.entity_type),
                    name=item.name,
                    description=item.description,
                )
            )

        return entities