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
    return MagicMock()


@pytest.fixture
def resolver(
    llm_service: MagicMock,
) -> ContextResolver:
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
    context = resolver.resolve(
        user_message="$result + 5",
        last_math_result=10,
    )

    assert context is not None
    assert context.expression == "$result+5"
    assert context.use_previous_result is True
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
    context = resolver.resolve(
        user_message=message,
        last_math_result=None,
    )

    assert context is None


def test_llm_math_response(
    resolver: ContextResolver,
    llm_service: MagicMock,
) -> None:
    llm_service.generate_response.return_value = {
        "content": json.dumps(
            {
                "is_math": True,
                "expression": "9-2",
                "language": "en",
                "use_previous_result": True,
            }
        )
    }

    context = resolver.resolve(
        user_message="Now subtract 2.",
        last_math_result=9,
    )

    assert context is not None
    assert context.expression == "9-2"
    assert context.language == "en"
    assert context.use_previous_result is True
    assert context.previous_result == 9

    llm_service.generate_response.assert_called_once()


def test_llm_returns_non_math(
    resolver: ContextResolver,
    llm_service: MagicMock,
) -> None:
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
    llm_service.generate_response.return_value = {
        "content": "invalid json",
    }

    context = resolver.resolve(
        user_message="Now subtract two.",
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
    assert context.previous_result == 15
    assert context.use_previous_result is True