import json
from unittest.mock import MagicMock

import pytest

from ai_assistant_platform.core.context_resolver import (
    ContextResolver,
)
from ai_assistant_platform.core.math_context import (
    MathContext,
)


@pytest.fixture
def llm_service() -> MagicMock:
    """Fixture that provides a mock instance of LLMService.

    Returns:
        MagicMock: A mock object simulating the LLM service layer.
    """
    return MagicMock()


@pytest.fixture
def resolver(
    llm_service: MagicMock,
) -> ContextResolver:
    """Fixture that initializes a ContextResolver instance with a mocked LLM service.

    Args:
        llm_service (MagicMock): Mock instance provided by the `llm_service` fixture.

    Returns:
        ContextResolver: An instance of ContextResolver configured for testing.
    """
    return ContextResolver(
        llm_service=llm_service,
    )


@pytest.mark.parametrize(
    ("message", "expression", "language"),
    [
        ("2 + 2", "2+2", "en"),
        ("10 - 5", "10-5", "en"),
        ("Quanto é 5 + 4?", "5+4", "pt"),
        ("Calcule: (10 + 5) * 2", "(10+5)*2", "pt"),
    ],
)
def test_resolve_direct_expression(
    resolver: ContextResolver,
    llm_service: MagicMock,
    message: str,
    expression: str,
    language: str,
) -> None:
    """Tests deterministic resolution of direct mathematical expressions.

    Verifies that explicit mathematical inputs bypass the LLM and directly produce 
    a valid MathContext object with expected properties.
    """
    context = resolver.resolve(
        user_message=message,
        last_math_result=None,
    )

    assert isinstance(context, MathContext)
    assert context.expression == expression
    assert context.language == language
    assert context.previous_result is None

    llm_service.generate_response.assert_not_called()


def test_resolve_expression_using_previous_result(
    resolver: ContextResolver,
    llm_service: MagicMock,
) -> None:
    """Tests resolution of direct expressions referencing a previous calculation result.

    Verifies that explicit usage of `$result` replaces the placeholder with the numerical
    value without invoking the LLM.
    """
    context = resolver.resolve(
        user_message="$result + 5",
        last_math_result=10,
    )

    assert context is not None
    assert context.expression == "10+5"
    assert context.use_previous_result is False
    assert context.previous_result == 10

    llm_service.generate_response.assert_not_called()


@pytest.mark.parametrize(
    "message",
    [
        "Tell me a joke.",
        "Who are you?",
        "Translate this text.",
        "Write a poem.",
    ],
)
def test_non_math_returns_none(
    resolver: ContextResolver,
    message: str,
) -> None:
    """Tests that non-mathematical messages are rejected early.

    Verifies that messages containing no mathematical intent or keywords yield None
    without reaching the LLM service.
    """
    context = resolver.resolve(
        user_message=message,
        last_math_result=None,
    )

    assert context is None


def test_llm_resolves_implicit_previous_result(
    resolver: ContextResolver,
    llm_service: MagicMock,
) -> None:
    """Tests LLM fallback resolution for implicit multi-turn mathematical queries.

    Verifies that conversational math prompts requiring context evaluation invoke
    the LLM service and properly substitute historical calculation results.
    """
    llm_service.generate_response.return_value = {
        "content": json.dumps(
            {
                "is_math": True,
                "expression": "$result/2",
                "language": "pt",
                "use_previous_result": True,
            }
        )
    }

    context = resolver.resolve(
        user_message="agora divida por 2",
        last_math_result=30,
    )

    assert context is not None
    assert context.expression == "30/2"
    assert context.language == "pt"
    assert context.use_previous_result is False
    assert context.previous_result == 30

    llm_service.generate_response.assert_called_once()


def test_llm_resolves_implicit_previous_result_without_calculating(
    resolver: ContextResolver,
    llm_service: MagicMock,
) -> None:
    """Tests that LLM-resolved expressions replace '$result' with literal numbers.

    Verifies that the returned expression string is fully populated and free of
    unresolved placeholder tokens.
    """
    llm_service.generate_response.return_value = {
        "content": json.dumps(
            {
                "is_math": True,
                "expression": "$result/2",
                "language": "pt",
                "use_previous_result": True,
            }
        )
    }

    context = resolver.resolve(
        user_message="agora divida por 2",
        last_math_result=30,
    )

    assert context is not None
    assert context.expression == "30/2"
    assert "$result" not in context.expression


def test_llm_returns_non_math(
    resolver: ContextResolver,
    llm_service: MagicMock,
) -> None:
    """Tests behavior when LLM classifies candidate text as non-mathematical.

    Verifies that when LLM evaluation outputs `is_math: False`, the resolver returns None.
    """
    llm_service.generate_response.return_value = {
        "content": json.dumps(
            {
                "is_math": False,
            }
        )
    }

    context = resolver.resolve(
        user_message="Tell me a joke.",
        last_math_result=None,
    )

    assert context is None


def test_invalid_json_returns_none(
    resolver: ContextResolver,
    llm_service: MagicMock,
) -> None:
    """Tests exception handling when LLM output cannot be parsed as valid JSON.

    Verifies that malformed JSON payloads from the LLM service result in a None return value.
    """
    llm_service.generate_response.return_value = {
        "content": "invalid json",
    }

    context = resolver.resolve(
        user_message="Now subtract 2.",
        last_math_result=10,
    )

    assert context is None


@pytest.mark.parametrize(
    "expression",
    [
        "",
        " ",
        "\n",
    ],
)
def test_empty_expression_returns_none(
    resolver: ContextResolver,
    llm_service: MagicMock,
    expression: str,
) -> None:
    """Tests that blank or whitespace-only expressions returned by the LLM are rejected.

    Args:
        expression (str): Blank or whitespace string variations.
    """
    llm_service.generate_response.return_value = {
        "content": json.dumps(
            {
                "is_math": True,
                "expression": expression,
                "language": "en",
            }
        )
    }

    context = resolver.resolve(
        user_message="calculate",
        last_math_result=None,
    )

    assert context is None


@pytest.mark.parametrize(
    ("language", "expected"),
    [
        ("pt", "pt"),
        ("PT", "pt"),
        ("pt-BR", "pt"),
        ("en-US", "en"),
        ("es-MX", "es"),
        ("fr", "fr"),
        ("de", "de"),
        ("ja", "ja"),
    ],
)
def test_language_normalization(
    resolver: ContextResolver,
    llm_service: MagicMock,
    language: str,
    expected: str,
) -> None:
    """Tests normalization of language strings returned by the LLM.

    Verifies that locale identifiers and uppercase language codes are converted
    to standardized two-letter ISO language codes.
    """
    llm_service.generate_response.return_value = {
        "content": json.dumps(
            {
                "is_math": True,
                "expression": "2+2",
                "language": language,
            }
        )
    }

    context = resolver.resolve(
        user_message="calculate",
        last_math_result=None,
    )

    assert context is not None
    assert context.language == expected


def test_default_language_is_english(
    resolver: ContextResolver,
    llm_service: MagicMock,
) -> None:
    """Tests fallback to English when the LLM returns a None language value."""
    llm_service.generate_response.return_value = {
        "content": json.dumps(
            {
                "is_math": True,
                "expression": "2+2",
                "language": None,
            }
        )
    }

    context = resolver.resolve(
        user_message="calculate",
        last_math_result=None,
    )

    assert context is not None
    assert context.language == "en"


def test_previous_result_is_preserved(
    resolver: ContextResolver,
    llm_service: MagicMock,
) -> None:
    """Tests that the previous mathematical result value is preserved in the MathContext.

    Verifies that the `previous_result` property retains the passed numerical value
    following successful LLM context resolution.
    """
    llm_service.generate_response.return_value = {
        "content": json.dumps(
            {
                "is_math": True,
                "expression": "$result*2",
                "language": "en",
                "use_previous_result": True,
            }
        )
    }

    context = resolver.resolve(
        user_message="Double it.",
        last_math_result=15,
    )

    assert context is not None
    assert context.expression == "15*2"
    assert context.previous_result == 15
    assert context.use_previous_result is False