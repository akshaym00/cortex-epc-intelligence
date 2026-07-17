"""
Centralized configuration for Project Cortex.

Reads settings from environment variables and the .env file,
providing a single source of truth for all configuration values.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env from project root
_dotenv_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=_dotenv_path, override=True)


class Settings:
    """
    Application-wide settings.

    All configuration is read from environment variables
    (with defaults for local development).
    """

    # OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-5-mini")

    # Mock mode (set to "true" for development without API calls)
    MOCK_MODE: bool = os.getenv("MOCK_MODE", "true").lower() == "true"

    # API
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))

    # CORS allowed origins
    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://localhost:5174",
    ]

    # Entity resolution
    ENTITY_SIMILARITY_THRESHOLD: float = float(
        os.getenv("ENTITY_SIMILARITY_THRESHOLD", "0.72")
    )

    # Deduplication
    DEDUPLICATION_THRESHOLD: float = float(
        os.getenv("DEDUPLICATION_THRESHOLD", "0.55")
    )

    # Pipeline
    MAX_WORKERS: int = int(os.getenv("MAX_WORKERS", "2"))
