from unittest.mock import MagicMock

import pytest

from ai_assistant_platform.core.math_context import MathContext
from ai_assistant_platform.orchestrators.chatbot_orchestrator import (
    ChatbotOrchestrator,
)


def test_process_math_message(
    orchestrator: ChatbotOrchestrator,
    context_resolver: MagicMock,
    mathematical_agent: MagicMock,
    writer_agent: MagicMock,
) -> None:
    context = MathContext(
        expression="2 + 2",
        language="en",
        use_previous_result=False,
        previous_result=None,
    )

    context_resolver.resolve.return_value = context
    mathematical_agent.execute.return_value = 4
    writer_agent.generate_response.return_value = "The result is 4."

    result = orchestrator.process_message(
        user_message="2 + 2",
        conversation_history=[],
    )

    context_resolver.resolve.assert_called_once_with(
        user_message="2 + 2",
        conversation_history=[],
    )

    mathematical_agent.execute.assert_called_once_with(
        expression="2 + 2",
    )

    writer_agent.generate_response.assert_called_once_with(
        result=4,
        language="en",
    )

    assert result["response"] == "The result is 4."
    assert result["metadata"]["math_result"] == 4
    assert result["metadata"]["expression"] == "2 + 2"
    assert result["metadata"]["language"] == "en"


def test_returns_refusal_when_context_is_none(
    orchestrator: ChatbotOrchestrator,
    context_resolver: MagicMock,
    mathematical_agent: MagicMock,
    writer_agent: MagicMock,
) -> None:
    context_resolver.resolve.return_value = None

    writer_agent.generate_refusal_response.return_value = (
        "I can only answer mathematical questions."
    )

    result = orchestrator.process_message(
        user_message="Tell me a joke.",
        conversation_history=[],
    )

    mathematical_agent.execute.assert_not_called()

    writer_agent.generate_refusal_response.assert_called_once()

    assert result["metadata"] == {}
    assert result["response"] == "I can only answer mathematical questions."


def test_propagates_math_exception(
    orchestrator: ChatbotOrchestrator,
    context_resolver: MagicMock,
    mathematical_agent: MagicMock,
) -> None:
    context = MathContext(
        expression="10 / 0",
        language="en",
        use_previous_result=False,
        previous_result=None,
    )

    context_resolver.resolve.return_value = context

    mathematical_agent.execute.side_effect = ValueError("Division by zero")

    with pytest.raises(ValueError):
        orchestrator.process_message(
            user_message="10 / 0",
            conversation_history=[],
        )


def test_calls_components_once(
    orchestrator: ChatbotOrchestrator,
    context_resolver: MagicMock,
    mathematical_agent: MagicMock,
    writer_agent: MagicMock,
) -> None:
    context = MathContext(
        expression="5 * 5",
        language="en",
        use_previous_result=False,
        previous_result=None,
    )

    context_resolver.resolve.return_value = context

    mathematical_agent.execute.return_value = 25

    writer_agent.generate_response.return_value = "The result is 25."

    orchestrator.process_message(
        user_message="5 * 5",
        conversation_history=[],
    )

    assert context_resolver.resolve.call_count == 1
    assert mathematical_agent.execute.call_count == 1
    assert writer_agent.generate_response.call_count == 1


@pytest.mark.parametrize(
    ("expression", "result"),
    [
        ("2 + 2", 4),
        ("10 - 3", 7),
        ("8 * 6", 48),
        ("20 / 5", 4),
    ],
)
def test_process_multiple_operations(
    orchestrator: ChatbotOrchestrator,
    context_resolver: MagicMock,
    mathematical_agent: MagicMock,
    writer_agent: MagicMock,
    expression: str,
    result: float,
) -> None:
    context = MathContext(
        expression=expression,
        language="en",
        use_previous_result=False,
        previous_result=None,
    )

    context_resolver.resolve.return_value = context

    mathematical_agent.execute.return_value = result

    writer_agent.generate_response.return_value = f"The result is {result}."

    response = orchestrator.process_message(
        user_message=expression,
        conversation_history=[],
    )

    assert response["metadata"]["math_result"] == result
    assert response["metadata"]["expression"] == expression


def test_preserves_language(
    orchestrator: ChatbotOrchestrator,
    context_resolver: MagicMock,
    mathematical_agent: MagicMock,
    writer_agent: MagicMock,
) -> None:
    context = MathContext(
        expression="5 + 4",
        language="pt",
        use_previous_result=False,
        previous_result=None,
    )

    context_resolver.resolve.return_value = context

    mathematical_agent.execute.return_value = 9

    writer_agent.generate_response.return_value = "O resultado é 9."

    orchestrator.process_message(
        user_message="Quanto é 5 + 4?",
        conversation_history=[],
    )

    writer_agent.generate_response.assert_called_once_with(
        result=9,
        language="pt",
    )


def test_returns_complete_metadata(
    orchestrator: ChatbotOrchestrator,
    context_resolver: MagicMock,
    mathematical_agent: MagicMock,  # Garantir que é MagicMock
    writer_agent: MagicMock,
) -> None:
    context = MathContext(
        expression="7 + 8",
        language="en",
        use_previous_result=False,
        previous_result=None,
    )

    context_resolver.resolve.return_value = context

    mathematical_agent.execute.return_value = 15

    # Lembre-se também de configurar o writer_agent com o dicionário estruturado
    writer_agent.generate_response.return_value = {
        "content": "The result is 15.",
        "usage": {},
    }

    response = orchestrator.process_message(
        user_message="7 + 8",
        conversation_history=[],
    )

    # Asserções de metadados completos
    assert response["metadata"]["math_result"] == 15
    assert response["metadata"]["expression"] == "7 + 8"
    assert response["metadata"]["language"] == "en"