"""
Pydantic schemas for relationship extraction responses.
"""

from pydantic import BaseModel


class RelationshipResponse(BaseModel):
    """
    Represents a single extracted relationship.
    """

    source: str

    relationship_type: str

    target: str


class RelationshipExtractionResponse(BaseModel):
    """
    Represents the complete relationship extraction response.
    """

    relationships: list[RelationshipResponse]