"""
Application configuration.

This module loads environment variables from a `.env` file and exposes
the configuration used by the application's language model providers.

Module Attributes:
    OPENAI_API_KEY (str | None):
        API key used for the OpenAI provider.

    GEMINI_API_KEY (str | None):
        API key used for the Gemini provider.

    OLLAMA_BASE_URL (str | None):
        Base URL of the Ollama server.

    LLM_PROVIDER (str):
        Selected language model provider.
        Defaults to ``"openai"``.

    MODEL_NAME (str):
        Name of the configured language model.
        Defaults to ``"gpt-5.4-mini"``.
"""

from dotenv import load_dotenv

import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")

LLM_PROVIDER = os.getenv(
    "LLM_PROVIDER",
    "openai",
)

MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "gpt-5.4-mini",
)
