from unittest.mock import MagicMock

import pytest

from ai_assistant_platform.core.math_context import MathContext
from ai_assistant_platform.orchestrators.chatbot_orchestrator import (
    ChatbotOrchestrator,
)


@pytest.fixture
def context_resolver() -> MagicMock:
    return MagicMock()


@pytest.fixture
def mathematical_agent() -> MagicMock:
    return MagicMock()


@pytest.fixture
def writer_agent() -> MagicMock:
    return MagicMock()


@pytest.fixture
def orchestrator(
    context_resolver: MagicMock,
    mathematical_agent: MagicMock,
    writer_agent: MagicMock,
) -> ChatbotOrchestrator:
    return ChatbotOrchestrator(
        context_resolver=context_resolver,
        mathematical_agent=mathematical_agent,
        writer_agent=writer_agent,
    )


def test_follow_up_subtraction(
    orchestrator: ChatbotOrchestrator,
    context_resolver: MagicMock,
    mathematical_agent: MagicMock,
    writer_agent: MagicMock,
) -> None:
    history = [
        {
            "role": "assistant",
            "content": "The result is 9.",
            "metadata": {
                "math_result": 9,
                "expression": "5 + 4",
                "language": "en",
            },
        }
    ]

    context_resolver.resolve.return_value = MathContext(
        expression="9 - 2",
        language="en",
        use_previous_result=True,
        previous_result=9,
    )

    mathematical_agent.execute.return_value = 7

    writer_agent.generate_response.return_value = {
        "content": "The result is 7.",
        "usage": {},
    }

    result = orchestrator.process_message(
        user_message="Now subtract 2.",
        conversation_history=history,
    )

    assert result["metadata"]["math_result"] == 7
    assert result["metadata"]["expression"] == "9 - 2"


def test_follow_up_multiplication(
    orchestrator: ChatbotOrchestrator,
    context_resolver: MagicMock,
    mathematical_agent: MagicMock,
    writer_agent: MagicMock,
) -> None:
    history = [
        {
            "role": "assistant",
            "metadata": {
                "math_result": 8,
                "language": "en",
            },
        }
    ]

    context_resolver.resolve.return_value = MathContext(
        expression="8 * 5",
        language="en",
        use_previous_result=True,
        previous_result=8,
    )

    mathematical_agent.execute.return_value = 40

    writer_agent.generate_response.return_value = {
        "content": "The result is 40.",
        "usage": {},
    }

    result = orchestrator.process_message(
        user_message="Multiply by 5.",
        conversation_history=history,
    )

    assert result["metadata"]["math_result"] == 40


def test_follow_up_division(
    orchestrator: ChatbotOrchestrator,
    context_resolver: MagicMock,
    mathematical_agent: MagicMock,
    writer_agent: MagicMock,
) -> None:
    history = [
        {
            "role": "assistant",
            "metadata": {
                "math_result": 56,
                "language": "en",
            },
        }
    ]

    context_resolver.resolve.return_value = MathContext(
        expression="56 / 7",
        language="en",
        use_previous_result=True,
        previous_result=56,
    )

    mathematical_agent.execute.return_value = 8

    writer_agent.generate_response.return_value = {
        "content": "The result is 8.",
        "usage": {},
    }

    result = orchestrator.process_message(
        user_message="Divide by 7.",
        conversation_history=history,
    )

    assert result["metadata"]["math_result"] == 8


@pytest.mark.parametrize(
    ("language", "expected"),
    [
        ("pt", "O resultado é 7."),
        ("en", "The result is 7."),
        ("es", "El resultado es 7."),
    ],
)
def test_language_is_preserved_between_turns(
    orchestrator: ChatbotOrchestrator,
    context_resolver: MagicMock,
    mathematical_agent: MagicMock,
    writer_agent: MagicMock,
    language: str,
    expected: str,
) -> None:
    history = [
        {
            "role": "assistant",
            "metadata": {
                "math_result": 9,
                "language": language,
            },
        }
    ]

    context_resolver.resolve.return_value = MathContext(
        expression="9 - 2",
        language=language,
        use_previous_result=True,
        previous_result=9,
    )

    mathematical_agent.execute.return_value = 7

    writer_agent.generate_response.return_value = {
        "content": expected,
        "usage": {},
    }

    result = orchestrator.process_message(
        user_message="continue",
        conversation_history=history,
    )

    assert result["response"] == expected
    assert result["metadata"]["language"] == language


def test_context_resolver_receives_history(
    orchestrator: ChatbotOrchestrator,
    context_resolver: MagicMock,
) -> None:
    history = [
        {
            "role": "assistant",
            "metadata": {
                "math_result": 15,
            },
        }
    ]

    context_resolver.resolve.return_value = None

    orchestrator.process_message(
        user_message="Continue.",
        conversation_history=history,
    )

    context_resolver.resolve.assert_called_once_with(
        user_message="Continue.",
        last_math_result=15,
    )


def test_previous_result_is_preserved_in_context(
    orchestrator: ChatbotOrchestrator,
    context_resolver: MagicMock,
    mathematical_agent: MagicMock,
    writer_agent: MagicMock,
) -> None:
    previous_result = 42

    context = MathContext(
        expression="42 + 8",
        language="en",
        use_previous_result=True,
        previous_result=previous_result,
    )

    context_resolver.resolve.return_value = context

    mathematical_agent.execute.return_value = 50

    writer_agent.generate_response.return_value = {
        "content": "The result is 50.",
        "usage": {},
    }

    orchestrator.process_message(
        user_message="Add 8.",
        conversation_history=[],
    )
