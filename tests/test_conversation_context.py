from unittest.mock import MagicMock

import pytest

from ai_assistant_platform.core.math_context import MathContext
from ai_assistant_platform.orchestrators.chatbot_orchestrator import (
    ChatbotOrchestrator,
)


@pytest.fixture
def context_resolver() -> MagicMock:
    """Fixture that provides a mock instance of ContextResolver.

    Returns:
        MagicMock: A mock object simulating the context resolution layer.
    """
    return MagicMock()


@pytest.fixture
def mathematical_agent() -> MagicMock:
    """Fixture that provides a mock instance of MathematicalAgent.

    Returns:
        MagicMock: A mock object simulating the math execution agent.
    """
    return MagicMock()


@pytest.fixture
def writer_agent() -> MagicMock:
    """Fixture that provides a mock instance of WriterAgent.

    Returns:
        MagicMock: A mock object simulating the response generation agent.
    """
    return MagicMock()


@pytest.fixture
def orchestrator(
    context_resolver: MagicMock,
    mathematical_agent: MagicMock,
    writer_agent: MagicMock,
) -> ChatbotOrchestrator:
    """Fixture that initializes a ChatbotOrchestrator instance with mocked dependencies.

    Args:
        context_resolver (MagicMock): Mock instance provided by the `context_resolver` fixture.
        mathematical_agent (MagicMock): Mock instance provided by the `mathematical_agent` fixture.
        writer_agent (MagicMock): Mock instance provided by the `writer_agent` fixture.

    Returns:
        ChatbotOrchestrator: An instance of ChatbotOrchestrator configured for testing.
    """
    llm_service = MagicMock()
    llm_service.provider_name = "mock"

    return ChatbotOrchestrator(
        context_resolver=context_resolver,
        mathematical_agent=mathematical_agent,
        writer_agent=writer_agent,
        llm_service=llm_service,
    )


def test_context_resolver_receives_last_math_result(
    orchestrator: ChatbotOrchestrator,
    context_resolver: MagicMock,
) -> None:
    """Tests that the orchestrator extracts the last math result from conversation history.

    Verifies that when processing a message, the orchestrator retrieves `math_result`
    from the metadata of the last assistant message and passes it to `context_resolver.resolve`.
    """
    history = [
        {
            "role": "assistant",
            "content": "O resultado é 30.",
            "metadata": {
                "math_result": 30,
                "expression": "20+10",
                "language": "pt",
            },
        }
    ]

    context_resolver.resolve.return_value = None

    orchestrator.process_message(
        user_message="agora divida por 2",
        conversation_history=history,
    )

    context_resolver.resolve.assert_called_once_with(
        user_message="agora divida por 2",
        last_math_result=30,
    )


def test_follow_up_division_uses_resolved_expression(
    orchestrator: ChatbotOrchestrator,
    context_resolver: MagicMock,
    mathematical_agent: MagicMock,
    writer_agent: MagicMock,
) -> None:
    """Tests the full orchestrator flow for a follow-up mathematical operation.

    Verifies that the orchestrator correctly coordinates expression resolution,
    mathematical execution, and response metadata generation for contextual follow-up prompts.
    """
    history = [
        {
            "role": "assistant",
            "content": "O resultado é 30.",
            "metadata": {
                "math_result": 30,
                "expression": "20+10",
                "language": "pt",
            },
        }
    ]

    context_resolver.resolve.return_value = MathContext(
        expression="30/2",
        language="pt",
        use_previous_result=False,
        previous_result=30,
    )

    mathematical_agent.execute.return_value = 15

    writer_agent.generate_response.return_value = {
        "content": "O resultado é 15.",
        "usage": {},
    }

    result = orchestrator.process_message(
        user_message="agora divida por 2",
        conversation_history=history,
    )

    mathematical_agent.execute.assert_called_once_with(
        expression="30/2",
    )

    assert result["metadata"]["math_result"] == 15
    assert result["metadata"]["expression"] == "30/2"
