"""
Event extraction engine.

Uses the LLM to detect project events from
documents such as reports, emails and meeting notes.
"""

from backend.ai.llm_client import LLMClient
from backend.extraction.event_parser import EventParser
from backend.models.event import ProjectEvent
from backend.prompts.extraction_prompts import ExtractionPrompts
from difflib import SequenceMatcher


class EventExtractor:
    """
    Extracts project events from documents.
    """

    def __init__(self):

        self.client = LLMClient()

    def extract(
        self,
        document: str,
        entity_names: list[str] | None = None,
    ) -> list[ProjectEvent]:
        """
        Extract events from a document.
        """

        prompt = ExtractionPrompts.event_extraction(
            document,
            entity_names,
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

        independent_events: list[ProjectEvent] = []

        for event in events:
            text = f"{event.title} {event.description}".casefold()
            is_consequence = (
                event.event_type.casefold() == "risk"
                and any(phrase in text for phrase in (
                    "potential impact",
                    "may affect",
                    "may be affected",
                    "risk of delay",
                ))
                and any(
                    existing.event_type.casefold() == "delay"
                    for existing in independent_events
                )
            )

            is_duplicate = any(
                SequenceMatcher(
                    None,
                    event.title.casefold(),
                    existing.title.casefold(),
                ).ratio() >= 0.72
                or (
                    event.affected_entity_name.casefold()
                    == existing.affected_entity_name.casefold()
                )
                for existing in independent_events
            )

            is_routine_transaction = (
                event.event_type.casefold() == "delivery"
                and any(phrase in text for phrase in (
                    " supplies ",
                    " supply by ",
                    "supplied by",
                ))
                and not any(word in text for word in ("delay", "late", "failed"))
            ) or (
                event.event_type.casefold() == "risk"
                and " requires " in text
                and not any(word in text for word in ("risk", "shortage", "unavailable"))
            )

            if not is_consequence and not is_duplicate and not is_routine_transaction:
                independent_events.append(event)

        return independent_events
