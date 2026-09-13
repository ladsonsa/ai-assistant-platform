from unittest.mock import MagicMock, patch

import pytest
from openai import RateLimitError

from ai_assistant_platform.llm.providers.openai_provider import OpenAIProvider


def test_openai_provider_requires_api_key() -> None:
    """Tests that OpenAIProvider raises RuntimeError when OPENAI_API_KEY is missing."""
    with patch(
        "ai_assistant_platform.llm.providers.openai_provider.OPENAI_API_KEY",
        None,
    ):
        with pytest.raises(
            RuntimeError,
            match="OPENAI_API_KEY is not configured",
        ):
            OpenAIProvider()


def test_openai_provider_initializes_client() -> None:
    """Tests that OpenAIProvider instantiates the OpenAI client with the given API key."""
    with (
        patch(
            "ai_assistant_platform.llm.providers.openai_provider.OPENAI_API_KEY",
            "test-key",
        ),
        patch(
            "ai_assistant_platform.llm.providers.openai_provider.OpenAI",
        ) as mock_openai,
    ):
        provider = OpenAIProvider()
        mock_openai.assert_called_once_with(api_key="test-key")
        assert provider.client is mock_openai.return_value


def test_openai_provider_generates_response() -> None:
    """Tests that generate_response executes correctly and extracts response content and usage metadata."""
    response = MagicMock()
    response.choices = [
        MagicMock(
            message=MagicMock(content="Hello"),
            finish_reason="stop",
        )
    ]
    response.usage = MagicMock(
        prompt_tokens=10,
        completion_tokens=5,
        total_tokens=15,
    )

    with (
        patch(
            "ai_assistant_platform.llm.providers.openai_provider.OPENAI_API_KEY",
            "test-key",
        ),
        patch(
            "ai_assistant_platform.llm.providers.openai_provider.OpenAI",
        ) as mock_openai,
    ):
        client = mock_openai.return_value
        client.chat.completions.create.return_value = response

        provider = OpenAIProvider()
        messages = [{"role": "user", "content": "Hello"}]

        result = provider.generate_response(messages)

        client.chat.completions.create.assert_called_once_with(
            model=provider.model_name,
            messages=messages,
            temperature=0,
            max_completion_tokens=512,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )

        assert result["content"] == "Hello"
        assert result["usage"]["provider"] == "openai"
        assert result["usage"]["model"] == provider.model_name
        assert result["usage"]["input_tokens"] == 10
        assert result["usage"]["output_tokens"] == 5
        assert result["usage"]["total_tokens"] == 15
        assert result["usage"]["finish_reason"] == "stop"


def test_openai_provider_returns_empty_content_when_response_content_is_none() -> None:
    """Tests that generate_response converts a None message content into an empty string."""
    response = MagicMock()
    response.choices = [
        MagicMock(
            message=MagicMock(content=None),
            finish_reason="stop",
        )
    ]
    response.usage = MagicMock()

    with (
        patch(
            "ai_assistant_platform.llm.providers.openai_provider.OPENAI_API_KEY",
            "test-key",
        ),
        patch(
            "ai_assistant_platform.llm.providers.openai_provider.OpenAI",
        ) as mock_openai,
    ):
        mock_openai.return_value.chat.completions.create.return_value = response

        provider = OpenAIProvider()
        result = provider.generate_response([])

        assert result["content"] == ""


def test_openai_provider_translates_rate_limit_error() -> None:
    """Tests that RateLimitError from OpenAI client is caught and re-raised as a descriptive RuntimeError."""
    response = MagicMock()
    response.status_code = 429
    response.request = MagicMock()
    error = RateLimitError(
        "rate limited",
        response=response,
        body=None,
    )

    with (
        patch(
            "ai_assistant_platform.llm.providers.openai_provider.OPENAI_API_KEY",
            "test-key",
        ),
        patch(
            "ai_assistant_platform.llm.providers.openai_provider.OpenAI",
        ) as mock_openai,
    ):
        mock_openai.return_value.chat.completions.create.side_effect = error

        provider = OpenAIProvider()

        with pytest.raises(
            RuntimeError,
            match="OpenAI rate limit exceeded",
        ):
            provider.generate_response([])


def test_openai_provider_translates_generic_error() -> None:
    """Tests that unexpected exceptions during API calls are wrapped and re-raised as RuntimeError."""
    with (
        patch(
            "ai_assistant_platform.llm.providers.openai_provider.OPENAI_API_KEY",
            "test-key",
        ),
        patch(
            "ai_assistant_platform.llm.providers.openai_provider.OpenAI",
        ) as mock_openai,
    ):
        mock_openai.return_value.chat.completions.create.side_effect = ValueError(
            "provider failure"
        )
        provider = OpenAIProvider()

        with pytest.raises(
            RuntimeError,
            match="OpenAI provider error: provider failure",
        ):
            provider.generate_response([])
