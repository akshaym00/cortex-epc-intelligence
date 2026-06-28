import os

import pytest

from backend.ai.llm_client import LLMClient


def test_openai_key_exists():

    assert os.getenv("OPENAI_API_KEY") is not None


def test_client_creation():

    client = LLMClient()

    assert client is not None