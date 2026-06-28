import json

from backend.extraction.event_schemas import (
    EventExtractionResponse,
)


class EventParser:

    @staticmethod
    def parse(response: str):

        data = json.loads(response)

        return EventExtractionResponse.model_validate(data)