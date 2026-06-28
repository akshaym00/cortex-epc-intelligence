"""
Pydantic schemas for LLM JSON responses.
"""

from pydantic import BaseModel


class EntityResponse(BaseModel):
    entity_type: str
    name: str
    description: str | None = None


class EntityExtractionResponse(BaseModel):
    entities: list[EntityResponse]