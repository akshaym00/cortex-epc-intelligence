"""
Parser for relationship extraction responses.
"""

import json

from backend.extraction.relationship_schemas import (
    RelationshipExtractionResponse,
)


class RelationshipParser:
    """
    Parses relationship JSON returned by the LLM.
    """

    @staticmethod
    def parse(response: str) -> RelationshipExtractionResponse:
        """
        Parse and validate a relationship extraction response.
        """

        data = json.loads(response)

        return RelationshipExtractionResponse.model_validate(data)