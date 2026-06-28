"""
LLM Client for Project Cortex.

This module provides a single interface for interacting
with Large Language Models.
"""

import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class LLMClient:
    """
    Wrapper around the OpenAI client.

    Future providers (Ollama, Azure OpenAI, Anthropic, Gemini)
    can be supported by replacing this implementation without
    changing the rest of the application.
    """

    def __init__(self) -> None:
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY not found in environment variables."
            )

        self.client = OpenAI(api_key=api_key)

    def generate(
        self,
        prompt: str,
        model: str = "gpt-5",
    ) -> str:
        """
        Generate a response from the language model.
        """

        response = self.client.responses.create(
            model=model,
            input=prompt,
        )

        return response.output_text