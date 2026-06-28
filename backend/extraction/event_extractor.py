"""
Event extraction engine.

Uses the LLM to detect project events from
documents such as reports, emails and meeting notes.
"""

from backend.ai.llm_client import LLMClient
from backend.extraction.event_parser import EventParser
from backend.models.event import ProjectEvent
from backend.prompts.extraction_prompts import ExtractionPrompts


class EventExtractor:
    """
    Extracts project events from documents.
    """

    def __init__(self):

        self.client = LLMClient()

    def extract(
        self,
        document: str,
    ) -> list[ProjectEvent]:
        """
        Extract events from a document.
        """

        prompt = ExtractionPrompts.event_extraction(
            document
        )

        response = self.client.generate(prompt)

        parsed = EventParser.parse(response)

        events: list[ProjectEvent] = []

        for item in parsed.events:

            events.append(
                ProjectEvent(
                    title=item.title,
                    event_type=item.event_type,
                    description=item.description,
                    affected_entity_name=item.affected_entity_name,
                    severity=item.severity,
                )
            )

        return events