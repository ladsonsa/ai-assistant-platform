from unittest.mock import MagicMock

import pytest

from ai_assistant_platform.agents.writer_agent import (
    WriterAgent,
)


@pytest.fixture
def llm_service() -> MagicMock:
    return MagicMock()


@pytest.fixture
def writer_agent(
    llm_service: MagicMock,
) -> WriterAgent:
    return WriterAgent(
        llm_service=llm_service,
    )


@pytest.mark.parametrize(
    ("language", "result", "response"),
    [
        ("en", 4, "The result is 4."),
        ("pt", 4, "O resultado é 4."),
        ("es", 4, "El resultado es 4."),
        ("fr", 4, "Le résultat est 4."),
    ],
)
def test_generate_response(
    writer_agent: WriterAgent,
    llm_service: MagicMock,
    language: str,
    result: float,
    response: str,
) -> None:
    llm_service.generate_response.return_value = {
        "content": response,
        "usage": {},
    }

    generated = writer_agent.generate_response(
        result=result,
        language=language,
    )

    expected = {
            "content": response,
            "usage": {},
        }
    assert generated == expected


@pytest.mark.parametrize(
    ("language", "message"),
    [
        ("en", "Division by zero."),
        ("pt", "Divisão por zero."),
        ("es", "División por cero."),
    ],
)
def test_generate_error_response(
    writer_agent: WriterAgent,
    llm_service: MagicMock,
    language: str,
    message: str,
) -> None:
    llm_service.generate_response.return_value = {
        "content": message,
        "usage": {},
    }

    response = writer_agent.generate_error_response(
        user_message=message,
        error="Division by zero",
    )
    
    expected = {
        "content": message,
        "usage": {},
    }
    assert response == expected



def test_llm_called_once(
    writer_agent: WriterAgent,
    llm_service: MagicMock,
) -> None:
    llm_service.generate_response.return_value = {
        "content": "The result is 9.",
        "usage": {},
    }

    writer_agent.generate_response(
        result=9,
        language="en",
    )

    assert llm_service.generate_response.call_count == 1


def test_returns_llm_content(
    writer_agent: WriterAgent,
    llm_service: MagicMock,
) -> None:
    expected = "Custom response."

    llm_service.generate_response.return_value = {
        "content": expected,
        "usage": {},
    }

    response = writer_agent.generate_response(
        result=10,
        language="en",
    )

    expected = {'content': 'Custom response.', 'usage': {}}
    assert response == expected


def test_propagates_llm_exception(
    writer_agent: WriterAgent,
    llm_service: MagicMock,
) -> None:
    llm_service.generate_response.side_effect = RuntimeError()

    with pytest.raises(RuntimeError):
        writer_agent.generate_response(
            result=10,
            language="en",
        )


@pytest.mark.parametrize(
    "language",
    [
        "pt",
        "en",
        "es",
        "fr",
        "de",
        "it",
        "ru",
        "ja",
        "zh",
        "ko",
        "ar",
    ],
)
def test_supported_languages(
    writer_agent: WriterAgent,
    llm_service: MagicMock,
    language: str,
) -> None:
    llm_service.generate_response.return_value = {
        "content": "ok",
        "usage": {},
    }

    writer_agent.generate_response(
        result=1,
        language=language,
    )

    llm_service.generate_response.assert_called()


def test_response_is_string(
    writer_agent: WriterAgent,
    llm_service: MagicMock,
) -> None:
    llm_service.generate_response.return_value = {
        "content": "The result is 42.",
        "usage": {},
    }

    response = writer_agent.generate_response(
        result=42,
        language="en",
    )

    assert isinstance(response, dict)
    assert isinstance(response["content"], str)
    assert response["content"] == "The result is 42."


def test_empty_response_is_allowed(
    writer_agent: WriterAgent,
    llm_service: MagicMock,
) -> None:
    llm_service.generate_response.return_value = {
        "content": "",
        "usage": {},
    }

    response = writer_agent.generate_response(
        result=1,
        language="en",
    )

    assert response["content"] == ""
