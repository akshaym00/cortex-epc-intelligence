"""
Document model for Project Cortex.

Represents a document that has been ingested into
the system for analysis.
"""

from pydantic import Field

from backend.models.base import CortexBaseModel


class Document(CortexBaseModel):
    """
    Represents a project document loaded into the system.
    """

    # Original filename
    filename: str

    # Raw text content extracted from the document
    content: str = ""

    # File extension (e.g. ".pdf", ".txt")
    file_type: str = ""

    # Size of the original file in bytes
    file_size: int = 0

    # Optional source path or URL
    source: str | None = None

    # Number of pages (for PDFs) or sections
    page_count: int = 0

    # Processing status
    status: str = "loaded"

    # Extraction metadata (e.g. loader used, parse time)
    processing_metadata: dict = Field(default_factory=dict)
