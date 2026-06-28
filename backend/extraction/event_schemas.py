"""
Schemas for event extraction.
"""

from pydantic import BaseModel


class EventResponse(BaseModel):

    title: str

    event_type: str

    description: str

    affected_entity_name: str

    severity: str


class EventExtractionResponse(BaseModel):

    events: list[EventResponse]