from unittest.mock import patch

import pytest

from ai_assistant_platform.llm.provider_factory import ProviderFactory
from ai_assistant_platform.llm.providers.gemini_provider import GeminiProvider
from ai_assistant_platform.llm.providers.ollama_provider import OllamaProvider
from ai_assistant_platform.llm.providers.openai_provider import OpenAIProvider


def test_provider_factory_creates_supported_providers() -> None:
    """Tests that ProviderFactory instantiates the correct provider for supported keys."""
    with (
        patch(
            "ai_assistant_platform.llm.providers.openai_provider.OPENAI_API_KEY",
            "test-key",
        ),
        patch(
            "ai_assistant_platform.llm.providers.openai_provider.OpenAI",
        ),
        patch(
            "ai_assistant_platform.llm.providers.gemini_provider.GEMINI_API_KEY",
            "test-key",
        ),
        patch(
            "ai_assistant_platform.llm.providers.gemini_provider.genai.Client",
        ),
        patch(
            "ai_assistant_platform.llm.providers.ollama_provider.Client",
        ),
    ):
        assert isinstance(
            ProviderFactory.get_provider("openai"),
            OpenAIProvider,
        )
        assert isinstance(
            ProviderFactory.get_provider("gemini"),
            GeminiProvider,
        )
        assert isinstance(
            ProviderFactory.get_provider("ollama"),
            OllamaProvider,
        )


def test_provider_factory_is_case_insensitive() -> None:
    """Tests that provider resolution handles case-insensitive string inputs."""
    with patch(
        "ai_assistant_platform.llm.providers.ollama_provider.Client",
    ):
        provider = ProviderFactory.get_provider("OLLAMA")
        assert isinstance(provider, OllamaProvider)


def test_provider_factory_rejects_unsupported_provider() -> None:
    """Tests that ProviderFactory raises ValueError when given an unknown provider name."""
    with pytest.raises(ValueError, match="Unsupported provider: unknown"):
        ProviderFactory.get_provider("unknown")
