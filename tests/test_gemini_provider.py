from unittest.mock import MagicMock, patch

import pytest

from ai_assistant_platform.llm.providers.gemini_provider import GeminiProvider


def test_gemini_provider_requires_api_key() -> None:
    """Tests that GeminiProvider raises RuntimeError when GEMINI_API_KEY is missing."""
    with patch(
        "ai_assistant_platform.llm.providers.gemini_provider.GEMINI_API_KEY",
        None,
    ):
        with pytest.raises(
            RuntimeError,
            match="GEMINI_API_KEY is not configured",
        ):
            GeminiProvider()


def test_gemini_provider_initializes_client() -> None:
    """Tests that GeminiProvider instantiates the genai client with the configured API key."""
    with (
        patch(
            "ai_assistant_platform.llm.providers.gemini_provider.GEMINI_API_KEY",
            "test-key",
        ),
        patch(
            "ai_assistant_platform.llm.providers.gemini_provider.genai.Client",
        ) as mock_client,
    ):
        provider = GeminiProvider()
        mock_client.assert_called_once_with(api_key="test-key")
        assert provider.client is mock_client.return_value


def test_gemini_provider_builds_prompt() -> None:
    """Tests that _build_prompt correctly formats system and user messages into a prompt string."""
    with (
        patch(
            "ai_assistant_platform.llm.providers.gemini_provider.GEMINI_API_KEY",
            "test-key",
        ),
        patch(
            "ai_assistant_platform.llm.providers.gemini_provider.genai.Client",
        ),
    ):
        provider = GeminiProvider()
        messages = [
            {"role": "system", "content": "Be concise."},
            {"role": "user", "content": "Hello"},
        ]

        assert provider._build_prompt(messages) == (
            "System: Be concise.\n\nUser: Hello\n\nAssistant:"
        )


def test_gemini_provider_generates_response() -> None:
    """Tests that generate_response sends prompt to Gemini and structures output and usage metadata."""
    response = MagicMock(
        text="Hello",
        finish_reason="STOP",
    )
    response.usage_metadata = MagicMock(
        prompt_token_count=10,
        candidates_token_count=5,
        total_token_count=15,
    )

    with (
        patch(
            "ai_assistant_platform.llm.providers.gemini_provider.GEMINI_API_KEY",
            "test-key",
        ),
        patch(
            "ai_assistant_platform.llm.providers.gemini_provider.genai.Client",
        ) as mock_client,
    ):
        mock_client.return_value.models.generate_content.return_value = response

        provider = GeminiProvider()
        messages = [{"role": "user", "content": "Hello"}]

        result = provider.generate_response(messages)

        mock_client.return_value.models.generate_content.assert_called_once_with(
            model=provider.model_name,
            contents="User: Hello\n\nAssistant:",
            config={
                "temperature": 0,
                "top_p": 1,
                "max_output_tokens": 512,
            },
        )

        assert result["content"] == "Hello"
        assert result["usage"]["provider"] == "gemini"
        assert result["usage"]["model"] == provider.model_name
        assert result["usage"]["input_tokens"] == 10
        assert result["usage"]["output_tokens"] == 5
        assert result["usage"]["total_tokens"] == 15
        assert result["usage"]["finish_reason"] == "STOP"


def test_gemini_provider_handles_missing_usage_metadata() -> None:
    """Tests that generate_response returns None for usage tokens when usage_metadata is missing."""
    response = MagicMock(text="Hello", finish_reason=None)
    response.usage_metadata = None

    with (
        patch(
            "ai_assistant_platform.llm.providers.gemini_provider.GEMINI_API_KEY",
            "test-key",
        ),
        patch(
            "ai_assistant_platform.llm.providers.gemini_provider.genai.Client",
        ) as mock_client,
    ):
        mock_client.return_value.models.generate_content.return_value = response

        provider = GeminiProvider()
        result = provider.generate_response([])

        assert result["content"] == "Hello"
        assert result["usage"]["input_tokens"] is None
        assert result["usage"]["output_tokens"] is None
        assert result["usage"]["total_tokens"] is None


def test_gemini_provider_translates_provider_error() -> None:
    """Tests that exceptions thrown during content generation are wrapped in a RuntimeError."""
    with (
        patch(
            "ai_assistant_platform.llm.providers.gemini_provider.GEMINI_API_KEY",
            "test-key",
        ),
        patch(
            "ai_assistant_platform.llm.providers.gemini_provider.genai.Client",
        ) as mock_client,
    ):
        mock_client.return_value.models.generate_content.side_effect = ValueError(
            "provider failure"
        )
        provider = GeminiProvider()

        with pytest.raises(
            RuntimeError,
            match="Gemini provider error: provider failure",
        ):
            provider.generate_response([])
