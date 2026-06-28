"""
Parser for converting LLM JSON responses into
validated Python objects.
"""

import json

from backend.extraction.schemas import EntityExtractionResponse


class ExtractionParser:
    """
    Parses structured JSON returned by the LLM.
    """

    @staticmethod
    def parse_entities(response: str) -> EntityExtractionResponse:
        data = json.loads(response)

        return EntityExtractionResponse.model_validate(data)