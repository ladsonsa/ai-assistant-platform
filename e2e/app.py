"""E2E test setup utilities and dependency overrides."""

from ai_assistant_platform.api.dependencies import get_chat_service
from main import app
from ai_assistant_platform.orchestrators.chatbot_orchestrator import (
    ChatbotOrchestrator,
)
from ai_assistant_platform.services import ChatService
from e2e.deterministic_llm_service import DeterministicLLMService


def get_e2e_chat_service() -> ChatService:
    """Factory dependency providing a ChatService configured with a deterministic LLM.

    Returns:
        ChatService: ChatService instance with deterministic responses for E2E tests.
    """
    llm_service = DeterministicLLMService()

    return ChatService(
        orchestrator=ChatbotOrchestrator(
            llm_service=llm_service,
        ),
    )


app.dependency_overrides[get_chat_service] = get_e2e_chat_service