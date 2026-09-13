from unittest.mock import patch

import pytest

from ai_assistant_platform.llm.providers.ollama_provider import OllamaProvider


def test_ollama_provider_initializes_client() -> None:
    """Tests that OllamaProvider instantiates the Ollama Client correctly."""
    with patch(
        "ai_assistant_platform.llm.providers.ollama_provider.Client",
    ) as mock_client:
        provider = OllamaProvider()
        mock_client.assert_called_once_with()
        assert provider.client is mock_client.return_value


def test_ollama_provider_generates_response() -> None:
    """Tests that generate_response calls Ollama client chat endpoint and maps result and token usage."""
    response = {
        "message": {
            "content": "Hello",
        },
        "prompt_eval_count": 10,
        "eval_count": 5,
        "eval_duration": 100,
        "load_duration": 200,
        "prompt_eval_duration": 50,
        "done_reason": "stop",
    }

    with patch(
        "ai_assistant_platform.llm.providers.ollama_provider.Client",
    ) as mock_client:
        mock_client.return_value.chat.return_value = response

        provider = OllamaProvider()
        messages = [{"role": "user", "content": "Hello"}]

        result = provider.generate_response(messages)

        mock_client.return_value.chat.assert_called_once_with(
            model=provider.model_name,
            messages=messages,
            options={
                "temperature": 0,
                "top_p": 1,
                "num_predict": 512,
            },
        )

        assert result["content"] == "Hello"
        assert result["usage"]["provider"] == "ollama"
        assert result["usage"]["model"] == provider.model_name
        assert result["usage"]["input_tokens"] == 10
        assert result["usage"]["output_tokens"] == 5
        assert result["usage"]["total_tokens"] == 15
        assert result["usage"]["eval_duration"] == 100
        assert result["usage"]["load_duration"] == 200
        assert result["usage"]["prompt_eval_duration"] == 50
        assert result["usage"]["finish_reason"] == "stop"


def test_ollama_provider_handles_missing_token_counts() -> None:
    """Tests that generate_response handles missing token and duration metrics gracefully."""
    response = {
        "message": {
            "content": "Hello",
        },
    }

    with patch(
        "ai_assistant_platform.llm.providers.ollama_provider.Client",
    ) as mock_client:
        mock_client.return_value.chat.return_value = response

        provider = OllamaProvider()
        result = provider.generate_response([])

        assert result["content"] == "Hello"
        assert result["usage"]["input_tokens"] is None
        assert result["usage"]["output_tokens"] is None
        assert result["usage"]["total_tokens"] == 0
        assert result["usage"]["eval_duration"] is None
        assert result["usage"]["load_duration"] is None
        assert result["usage"]["prompt_eval_duration"] is None
        assert result["usage"]["finish_reason"] is None


def test_ollama_provider_translates_provider_error() -> None:
    """Tests that exceptions thrown during Ollama API execution are re-raised as RuntimeError."""
    with patch(
        "ai_assistant_platform.llm.providers.ollama_provider.Client",
    ) as mock_client:
        mock_client.return_value.chat.side_effect = ValueError("provider failure")
        provider = OllamaProvider()

        with pytest.raises(
            RuntimeError,
            match="Ollama provider error: provider failure",
        ):
            provider.generate_response([])
