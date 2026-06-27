"""
Base model for all Project Cortex domain models.

Every model in the system (Project, Entity, Event, Document,
Relationship, Impact, Recommendation, etc.) inherits from this class.
"""

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


class CortexBaseModel(BaseModel):
    """
    Common fields shared by every model in Project Cortex.
    """

    # Unique identifier
    id: str = Field(
        default_factory=lambda: str(uuid4()),
        description="Globally unique identifier."
    )

    # Object creation timestamp
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="UTC timestamp when the object was created."
    )

    # Last modification timestamp
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="UTC timestamp when the object was last updated."
    )

    # Flexible storage for additional information
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Optional metadata associated with the object."
    )

    model_config = {
        # Reject unknown fields
        "extra": "forbid",

        # Validate whenever attributes are modified
        "validate_assignment": True,

        # Allow construction from attributes of other objects
        "from_attributes": True,
    }