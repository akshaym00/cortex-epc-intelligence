"""
LLM Client for Project Cortex.

Supports:
1. Mock mode (development)
2. OpenAI Responses API (production)
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

# ---------------------------------------------------
# Load the project's .env file explicitly
# ---------------------------------------------------

dotenv_path = Path(__file__).resolve().parents[2] / ".env"

print(f"Loading .env from: {dotenv_path}")

load_dotenv(dotenv_path=dotenv_path, override=True)

api_key = os.getenv("OPENAI_API_KEY")
mock_mode = os.getenv("MOCK_MODE")

print("MOCK_MODE =", mock_mode)


class LLMClient:
    """
    Wrapper around language model providers.
    """

    def __init__(self) -> None:

        self.mock_mode = (
            os.getenv("MOCK_MODE", "true").lower() == "true"
        )

        if self.mock_mode:
            self.client = None
            print("Running in MOCK MODE")
            return

        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY not found in .env"
            )

        self.client = OpenAI(
            api_key=api_key,
        )

        print("Connected to OpenAI API")

    def generate(
        self,
        prompt: str,
        model: str = "gpt-5",
    ) -> str:
        """
        Generate a response from the language model.
        """

        if self.mock_mode:
            return self._mock_response(prompt)

        response = self.client.responses.create(
            model=model,
            input=prompt,
        )

        output = response.output_text

        if not output.strip():
            raise ValueError(
                "OpenAI returned an empty response."
            )

        return output

    def _mock_response(
        self,
        prompt: str,
    ) -> str:
        """
        Temporary mock responses used during development.
        """

        return "MOCK_RESPONSE"
