from collections.abc import Generator
from typing import Any
from unittest.mock import MagicMock

import pytest

from ai_assistant_platform.agents.mathematical_agent import MathematicalAgent
from ai_assistant_platform.agents.writer_agent import WriterAgent
from ai_assistant_platform.core.context_resolver import ContextResolver
from ai_assistant_platform.llm.llm_service import LLMService
from ai_assistant_platform.orchestrators.chatbot_orchestrator import ChatbotOrchestrator


@pytest.fixture
def llm_service() -> MagicMock:
    service = MagicMock(spec=LLMService)
    service.provider_name = "mock"
    service.generate_response.return_value = {
        "content": '{"is_math": true, "expression": "5 + 4", "language": "en"}',
        "usage": {},
    }
    return service


@pytest.fixture
def context_resolver() -> MagicMock:
    resolver = MagicMock(spec=ContextResolver)
    resolver.resolve.return_value = MagicMock(
        expression="5 + 4",
        language="en",
        use_previous_result=False,
    )
    return resolver


@pytest.fixture
def mathematical_agent() -> MagicMock:
    # Padronizado como Mock para o Orquestrador
    agent = MagicMock(spec=MathematicalAgent)
    agent.execute.return_value = 9.0
    return agent


@pytest.fixture
def writer_agent() -> MagicMock:
    # Padronizado como Mock para o Orquestrador
    agent = MagicMock(spec=WriterAgent)
    agent.generate_response.return_value = {
        "content": "The result is 9.",
        "usage": {},
    }
    return agent


@pytest.fixture
def orchestrator(
    context_resolver: MagicMock,
    mathematical_agent: MagicMock,
    writer_agent: MagicMock,
    llm_service: MagicMock,
) -> ChatbotOrchestrator:
    return ChatbotOrchestrator(
        llm_service=llm_service,
        context_resolver=context_resolver,
        mathematical_agent=mathematical_agent,
        writer_agent=writer_agent,
    )


@pytest.fixture
def conversation_history() -> list[dict[str, Any]]:
    return []


@pytest.fixture
def assistant_history() -> list[dict[str, Any]]:
    return [
        {
            "role": "assistant",
            "content": "The result is 9.",
            "metadata": {
                "math_result": 9.0,
                "expression": "5 + 4",
                "language": "en",
            },
        }
    ]


@pytest.fixture
def portuguese_history() -> list[dict[str, Any]]:
    return [
        {
            "role": "assistant",
            "content": "O resultado é 9.",
            "metadata": {
                "math_result": 9.0,
                "expression": "5 + 4",
                "language": "pt",
            },
        }
    ]


@pytest.fixture
def spanish_history() -> list[dict[str, Any]]:
    return [
        {
            "role": "assistant",
            "content": "El resultado es 9.",
            "metadata": {
                "math_result": 9.0,
                "expression": "5 + 4",
                "language": "es",
            },
        }
    ]


@pytest.fixture
def llm_math_response() -> dict[str, Any]:
    return {
        "content": ('{"is_math": true, "expression": "5 + 4", "language": "en"}'),
        "usage": {},
    }


@pytest.fixture
def llm_non_math_response() -> dict[str, Any]:
    return {
        "content": ('{"is_math": false, "expression": null, "language": "en"}'),
        "usage": {},
    }


@pytest.fixture(autouse=True)
def reset_mock(
    llm_service: MagicMock,
) -> Generator[None, None, None]:
    yield
    llm_service.reset_mock()
